cmake_minimum_required(VERSION 3.15)
project(toyos C ASM)

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_ASM_COMPILER aarch64-linux-gnu-as)
set(CMAKE_LINKER aarch64-linux-gnu-ld)

# Set linker script
set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/linker.ld)

# Source files
file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS
    "src/*.c"
    "src/*.s"
)

add_executable(toyos.elf ${SOURCES})

target_include_directories(toyos.elf PRIVATE src/include)

target_link_options(toyos.elf PRIVATE
        -nostdlib
        -static
        -T ${LINKER_SCRIPT}
)

add_custom_command(TARGET toyos.elf POST_BUILD
    COMMAND aarch64-linux-gnu-objcopy -O binary toyos.elf toyos.bin
)

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

add_custom_target(gdb
    COMMAND gdb-multiarch -x ${CMAKE_SOURCE_DIR}/gdb.script
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    DEPENDS toyos.elf
    COMMENT "Starting GDB with debug.gdb for toyos.elf"
)
