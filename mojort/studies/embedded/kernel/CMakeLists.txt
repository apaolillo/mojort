cmake_minimum_required(VERSION 3.15)
project(toyos C ASM)

# --- Cross toolchain (AArch64) ---
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_ASM_COMPILER aarch64-linux-gnu-as)
set(CMAKE_LINKER aarch64-linux-gnu-ld)

# --- Linker script ---
set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/linker.ld)

# --- Mojo cross-compile settings ---
# Adjust these if you want Linux userland instead of bare-metal:
#   set(MOJO_TARGET_TRIPLE aarch64-unknown-linux-gnu)
set(MOJO_CMD /home/user/.mojort/.venv/bin/mojo CACHE STRING "Path to the Mojo compiler")
set(MOJO_TARGET_TRIPLE aarch64-none-elf CACHE STRING "Mojo target triple")
set(MOJO_MCPU cortex-a72 CACHE STRING "Mojo target CPU")

# --- Sources: C and ASM ---
file(GLOB_RECURSE CSOURCES  CONFIGURE_DEPENDS "src/*.c")
file(GLOB_RECURSE ASMSOURCES CONFIGURE_DEPENDS "src/*.s")

# --- Sources: Mojo (.mojo -> .o via custom commands) ---
file(GLOB_RECURSE MOJO_SOURCES CONFIGURE_DEPENDS "src/*.mojo")
set(MOJO_OBJECTS)

foreach(MSRC IN LISTS MOJO_SOURCES)
    # Mirror the src/ layout in the build tree for object placement
    file(RELATIVE_PATH rel "${CMAKE_SOURCE_DIR}" "${MSRC}")
    get_filename_component(rel_dir "${rel}" DIRECTORY)
    get_filename_component(base "${MSRC}" NAME_WE)
    set(MOBJ "${CMAKE_CURRENT_BINARY_DIR}/${rel_dir}/${base}.o")

    add_custom_command(
        OUTPUT "${MOBJ}"
        COMMAND ${CMAKE_COMMAND} -E make_directory "${CMAKE_CURRENT_BINARY_DIR}/${rel_dir}"
        COMMAND ${MOJO_CMD} build "${MSRC}"
                --emit object
                --target-triple ${MOJO_TARGET_TRIPLE}
                --mcpu ${MOJO_MCPU}
                -o "${MOBJ}"
        DEPENDS "${MSRC}"
        COMMENT "Mojo: ${rel} -> ${MOBJ}"
        VERBATIM
    )
    list(APPEND MOJO_OBJECTS "${MOBJ}")
endforeach()

# --- Target ---
add_executable(toyos.elf ${CSOURCES} ${ASMSOURCES} ${MOJO_OBJECTS})
target_include_directories(toyos.elf PRIVATE src/include)

# Linker options (bare-metal style)
target_link_options(toyos.elf PRIVATE
    -nostdlib
    -static
    -T ${LINKER_SCRIPT}
)

# --- Post build: ELF -> BIN ---
add_custom_command(TARGET toyos.elf POST_BUILD
    COMMAND aarch64-linux-gnu-objcopy -O binary toyos.elf toyos.bin
    COMMENT "objcopy: toyos.elf -> toyos.bin"
)

# --- Run in QEMU (ELF) ---
add_custom_target(run-qemu-elf
    COMMAND qemu-system-aarch64
        -M virt
        -cpu cortex-a72
        -nographic
        -serial mon:stdio
        -kernel ${CMAKE_CURRENT_BINARY_DIR}/toyos.elf
        -semihosting
        -s
    DEPENDS toyos.elf
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Running toyos.elf in QEMU"
)

# --- Debug in QEMU (ELF, -S waits for GDB) ---
add_custom_target(debug-qemu-elf
    COMMAND qemu-system-aarch64
        -M virt
        -cpu cortex-a72
        -nographic
        -serial mon:stdio
        -kernel ${CMAKE_CURRENT_BINARY_DIR}/toyos.elf
        -semihosting
        -s
        -S
    DEPENDS toyos.elf
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Debugging toyos.elf in QEMU"
)

# --- GDB (assumes you have a gdb.script) ---
add_custom_target(gdb
    COMMAND gdb-multiarch -x ${CMAKE_SOURCE_DIR}/gdb.script
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    DEPENDS toyos.elf
    COMMENT "Starting GDB with debug.gdb for toyos.elf"
)
