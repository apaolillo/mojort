import subprocess
from pathlib import Path


def language2foldername(language: str) -> str:
    """Map language identifier to its source folder name."""
    language_map = {
        "cpp-gcc": "cpp",
        "cpp-clang": "cpp",
        "c-gcc": "c",
        "c-clang": "c",
        "rust": "rust",
        "mojo": "mojo",
    }
    return language_map.get(language, language)


def get_build_command(
    language: str,
    opt_level: str,
    src_filename: str,
) -> str:
    """
    Generate build command for a given language and optimization level.

    Args:
        language: Language/compiler combination (e.g., "cpp-gcc", "c-clang", "rust", "mojo")
        opt_level: Optimization level ("O0", "O1", "O2", "O3", "Ofast")
        src_filename: Name of the source file (without extension)

    Returns:
        Build command string
    """
    mojo_bin = "/home/user/.mojort/.venv/bin"

    # Map optimization levels to compiler flags
    opt_flag = f"-{opt_level}" if opt_level != "O0" else ""

    cmd = ""
    match language:
        case "cpp-gcc":
            cmd = f"g++ {opt_flag} {src_filename}.cpp -o {src_filename}"

        case "cpp-clang":
            cmd = f"clang++ {opt_flag} {src_filename}.cpp -o {src_filename}"

        case "c-gcc":
            cmd = f"gcc {opt_flag} -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"

        case "c-clang":
            cmd = f"clang {opt_flag} -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"

        case "rust":
            # Rust uses custom profiles for different optimization levels
            profile_map = {"O0": "a", "O1": "b", "O2": "c", "O3": "d"}
            profile = profile_map.get(opt_level, "a")
            cmd = f"cargo build --profile {profile}"

        case "mojo":
            # Mojo optimization levels: 0, 1, 2, 3
            opt_num = opt_level[1] if opt_level.startswith("O") else "0"
            cmd = f"{mojo_bin}/mojo build -O {opt_num} -o {src_filename} {src_filename}.mojo"

        case _:
            raise ValueError(f"Unknown language '{language}'")

    cmd = cmd.strip()
    return cmd


def get_object_build_command(
    language: str,
    opt_level: str,
    src_filename: str,
) -> str:
    """
    Generate build command for object files (for size benchmarking).

    Args:
        language: Language/compiler combination (e.g., "cpp-gcc", "c-clang", "rust", "mojo")
        opt_level: Optimization level ("O0", "O1", "O2", "O3", "Ofast")
        src_filename: Name of the source file (without extension)

    Returns:
        Build command string for object file generation
    """
    mojo_bin = "/home/user/.mojort/.venv/bin"

    # Map optimization levels to compiler flags
    opt_flag = f"-{opt_level}" if opt_level != "O0" else ""

    sf = src_filename

    match language:
        case "cpp-gcc":
            cmd = f"g++ {opt_flag} {sf}.cpp -c -o {sf}.o".strip()

        case "cpp-clang":
            cmd = f"clang++ {opt_flag} {sf}.cpp -c -o {sf}.o".strip()

        case "c-gcc":
            cmd = f"gcc {opt_flag} -std=c11 -D_GNU_SOURCE {sf}.c -c -lm -o {sf}.o".strip()

        case "c-clang":
            cmd = f"clang {opt_flag} -std=c11 -D_GNU_SOURCE {sf}.c -c -lm -o {sf}.o".strip()

        case "rust":
            # Rust uses custom profiles for different optimization levels
            profile_map = {"O0": "a", "O1": "b", "O2": "c", "O3": "d"}
            profile = profile_map.get(opt_level, "a")
            cmd = f"cargo rustc --profile {profile} -- --emit obj={sf}.o"

        case "mojo":
            # Mojo optimization levels: 0, 1, 2, 3
            opt_num = opt_level[1] if opt_level.startswith("O") else "0"
            cmd = (
                f"{mojo_bin}/mojo build "
                f"-O {opt_num} "
                f"--debug-level none "
                f"--emit object "
                f"-o {sf}.o {sf}.mojo"
            )

        case _:
            raise ValueError(f"Unknown language '{language}'")

    return cmd


def stress_prerun_hook(
    build_variables,
    run_variables,
    other_variables,
    record_data_dir,
) -> None:
    # TODO use benchkit internal primitives
    subprocess.Popen(
        "stress-ng --cpu 0 --cpu-method all -t 65",
        shell=True,
        stdout=None,
        stderr=None,
    )


def rust_add_executable_path(
    language: str,
    filename: str,
    path: Path,
    opt_level: str = "O0",
) -> Path:
    """
    Add Rust-specific executable path based on optimization level.

    Args:
        language: Language identifier
        filename: Name of the executable
        path: Base path
        opt_level: Optimization level (O0, O1, O2, O3)

    Returns:
        Updated path with Rust target directory
    """
    if not language.startswith("rust"):
        return path

    # Map optimization levels to Rust profiles
    profile_map = {"O0": "a", "O1": "b", "O2": "c", "O3": "d"}
    profile = profile_map.get(opt_level, "a")

    return path / Path(f"{filename}/target/{profile}/")
