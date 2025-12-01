
from pathlib import Path
import subprocess


def language2foldername(language: str) -> str:
    # -O flags are modeled as a seperate language but the folder is still the same
    if language.startswith("cpp"):
        language_folder = "cpp"
    elif language.startswith("mojo"):
        language_folder = "mojo"
    elif language.startswith("c-"):
        language_folder = "c"
    elif language.startswith("rust"):
        language_folder = "rust"
    else:
        language_folder = language
    return language_folder

def language2cmdline(
    language: str,
    src_filename: str,
) -> str:
    mojo_bin = "/home/user/.mojort/.venv/bin"

    match language:
        # --- C++ GCC
        case "cpp -Ofast":
            cmd = f"g++ -Ofast {src_filename}.cpp -o {src_filename}"
        case "cpp-gcc -O3":
            cmd = f"g++ -O3 {src_filename}.cpp -o {src_filename}"
        case "cpp-gcc -O2":
            cmd = f"g++ -O2 {src_filename}.cpp -o {src_filename}"
        case "cpp-gcc -O1":
            cmd = f"g++ -O1 {src_filename}.cpp -o {src_filename}"
        case "cpp-gcc":
            cmd = f"g++ {src_filename}.cpp -o {src_filename}"

        # --- C++ Clang
        case "cpp-clang -O3":
            cmd = f"clang++ -O3 {src_filename}.cpp -o {src_filename}"
        case "cpp-clang -O2":
            cmd = f"clang++ -O2 {src_filename}.cpp -o {src_filename}"
        case "cpp-clang -O1":
            cmd = f"clang++ -O1 {src_filename}.cpp -o {src_filename}"
        case "cpp-clang":
            cmd = f"clang++ {src_filename}.cpp -o {src_filename}"

        # --- C GCC
        case "c-gcc -O3":
            cmd = f"gcc -O3 -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"
        case "c-gcc -O2":
            cmd = f"gcc -O2 -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"
        case "c-gcc -O1":
            cmd = f"gcc -O1 -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"
        case "c-gcc":
            cmd = f"gcc -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"

        # --- C Clang
        case "c-clang -O3":
            cmd = f"clang -O3 -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"
        case "c-clang -O2":
            cmd = f"clang -O2 -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"
        case "c-clang -O1":
            cmd = f"clang -O1 -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"
        case "c-clang":
            cmd = f"clang -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -o {src_filename}"

        # --- Rust
        case "rust -O3":
            cmd = f"cargo build --profile d"
        case "rust -O2":
            cmd = f"cargo build --profile c"
        case "rust -O1":
            cmd = f"cargo build --profile b"
        case "rust":
            cmd = f"cargo build --profile a"

        # --- Mojo
        case "mojo":
            cmd = f"{mojo_bin}/mojo build -O 0 -o {src_filename} {src_filename}.mojo"
        case "mojo -O1":
            cmd = f"{mojo_bin}/mojo build -O 1 -o {src_filename} {src_filename}.mojo"
        case "mojo -O2":
            cmd = f"{mojo_bin}/mojo build -O 2 -o {src_filename} {src_filename}.mojo"
        case "mojo -O3":
            cmd = f"{mojo_bin}/mojo build -O 3 -o {src_filename} {src_filename}.mojo"

        case _:
            raise ValueError(f"Unknown language '{language}'")

    return cmd

def stress_prerun_hook(
        build_variables,
        run_variables,
        other_variables,
        record_data_dir,
    ) -> None:
     subprocess.Popen("stress-ng --cpu 0 --cpu-method all -t 65", shell=True,stdout=None,stderr=None)


def rust_add_executable_path(
    language: str,
    filename:str,
    path: Path,
) -> Path:

    match language:

        # --- Rust
        case "rust -O3":
            path = path / Path(f"{filename}/target/d/")
        case "rust -O2":
            path = path / Path(f"{filename}/target/c/")
        case "rust -O1":
            path = path / Path(f"{filename}/target/b/")
        case "rust":
            path = path / Path(f"{filename}/target/a/")

    return path
