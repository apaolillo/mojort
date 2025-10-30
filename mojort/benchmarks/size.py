import re
from pathlib import Path
import subprocess
from typing import Any, Dict, List, Iterable
from mojort.utils import language2cmdline, language2foldername, rust_add_build_path
from benchkit.benchmark import Benchmark, RecordResult, CommandWrapper
from benchkit.platforms import Platform
from benchkit.utils.dir import gitmainrootdir
from benchkit.utils.types import PathType


class SizeBench(Benchmark):
    def __init__(
        self,
        platform: Platform,
        command_wrappers: Iterable[CommandWrapper] = [],
    ) -> None:
        super().__init__(
            command_wrappers=command_wrappers,
            command_attachments=(),
            shared_libs=(),
            pre_run_hooks=(),
            post_run_hooks=(),
        )
        self.platform = platform
        self._src_path = gitmainrootdir() / "benchmarks"
        self._benchmark_dir = Path("/home/user/workspace/mojort/benchmarks")

    @property
    def bench_src_path(self) -> Path:
        return self._src_path

    def build_bench(
        self,
        language: str,
        src_filename: str,
        **kwargs,
    ) -> None:
        language_folder = language2foldername(language)
        language_folder = rust_add_build_path(language,src_filename,language_folder)

        lg_bench_dir = self._benchmark_dir / language_folder
        if not self.platform.comm.isdir(path=lg_bench_dir):
            raise ValueError(
                f"Language '{language_folder}' not found as '{lg_bench_dir}' is not a directory"
            )
        mojo_bin = "/home/user/.mojort/.venv/bin"

        match language:
            # --- C++ GCC
            case "cpp -Ofast":
                cmd = f"g++ -Ofast {src_filename}.cpp -c -o {src_filename}.o"
            case "cpp-gcc -O3":
                cmd = f"g++ -O3 {src_filename}.cpp -c -o {src_filename}.o"
            case "cpp-gcc -O2":
                cmd = f"g++ -O2 {src_filename}.cpp -c -o {src_filename}.o"
            case "cpp-gcc -O1":
                cmd = f"g++ -O1 {src_filename}.cpp -c -o {src_filename}.o"
            case "cpp-gcc":
                cmd = f"g++ {src_filename}.cpp -c -o {src_filename}.o"

            # --- C++ Clang
            case "cpp-clang -O3":
                cmd = f"clang++ -O3 {src_filename}.cpp -c -o {src_filename}.o"
            case "cpp-clang -O2":
                cmd = f"clang++ -O2 {src_filename}.cpp -c -o {src_filename}.o"
            case "cpp-clang -O1":
                cmd = f"clang++ -O1 {src_filename}.cpp -c -o {src_filename}.o"
            case "cpp-clang":
                cmd = f"clang++ {src_filename}.cpp -c -o {src_filename}.o"

            # --- C GCC
            case "c-gcc -O3":
                cmd = f"gcc -O3 -std=c11 -D_GNU_SOURCE {src_filename}.c -c -lm -o {src_filename}.o"
            case "c-gcc -O2":
                cmd = f"gcc -O2 -std=c11 -D_GNU_SOURCE {src_filename}.c -c -lm -o {src_filename}.o"
            case "c-gcc -O1":
                cmd = f"gcc -O1 -std=c11 -D_GNU_SOURCE {src_filename}.c -c -lm -o {src_filename}.o"
            case "c-gcc":
                cmd = f"gcc -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -c -o {src_filename}.o"

            # --- C Clang
            case "c-clang -O3":
                cmd = f"clang -O3 -std=c11 -D_GNU_SOURCE {src_filename}.c -c -lm -o {src_filename}.o"
            case "c-clang -O2":
                cmd = f"clang -O2 -std=c11 -D_GNU_SOURCE {src_filename}.c -c -lm -o {src_filename}.o"
            case "c-clang -O1":
                cmd = f"clang -O1 -std=c11 -D_GNU_SOURCE {src_filename}.c -c -lm -o {src_filename}.o"
            case "c-clang":
                cmd = f"clang -std=c11 -D_GNU_SOURCE {src_filename}.c -lm -c -o {src_filename}.o"

            # --- Rust
            case "rust -O3":
                cmd = f"cargo rustc --profile d -- --emit obj={src_filename}.o"
            case "rust -O2":
                cmd = f"cargo rustc --profile b -- --emit obj={src_filename}.o"
            case "rust -O1":
                cmd = f"cargo rustc --profile c -- --emit obj={src_filename}.o"
            case "rust":
                cmd = f"cargo rustc --profile a -- --emit obj={src_filename}.o"

            # --- Mojo
            case "mojo":
                cmd = f"{mojo_bin}/mojo build -O 0 --debug-level none --emit object -o {src_filename}.o {src_filename}.mojo"
            case "mojo -O1":
                cmd = f"{mojo_bin}/mojo build -O 1 --debug-level none --emit object -o {src_filename}.o {src_filename}.mojo"
            case "mojo -O2":
                cmd = f"{mojo_bin}/mojo build -O 2 --debug-level none --emit object -o {src_filename}.o {src_filename}.mojo"
            case "mojo -O3":
                cmd = f"{mojo_bin}/mojo build -O 3 --debug-level none --emit object -o {src_filename}.o {src_filename}.mojo"

        self.platform.comm.shell(
            command=cmd,
            current_dir=lg_bench_dir,
            output_is_log=True,
        )

    def single_run(
        self,
        build_variables: Dict[str, Any],
        **kwargs,
    ) -> str:
        language: str = build_variables["language"]
        language_folder = language2foldername(language)

        src_filename: str = build_variables["src_filename"]
        lg_bench_dir = self._benchmark_dir / language_folder
        lg_bench_dir = rust_add_build_path(language,src_filename,lg_bench_dir)

        # command to analyze the file size
        cmd = ["du","-b",f"./{src_filename}.o",]

        # strip the file
        self.platform.comm.shell(f"strip -s ./{src_filename}.o",current_dir=lg_bench_dir)

        # added command to get the object dump for debugging
        # self.platform.comm.shell(f'objdump -d ./{src_filename} > ./{src_filename}.dmp',shell = True,current_dir=lg_bench_dir)


        environment = self._preload_env(**kwargs)
        wrapped_run_command, wrapped_environment = self._wrap_command(
            run_command=cmd,
            environment=environment,
            **kwargs,
        )

        output = self.run_bench_command(
            run_command=cmd,
            wrapped_run_command=wrapped_run_command,
            current_dir=lg_bench_dir,
            environment=environment,
            wrapped_environment=wrapped_environment,
            print_output=False,
        )

        return output

    def parse_output_to_results(
        self,
        command_output: str,
        build_variables: Dict[str, Any],
        run_variables: Dict[str, Any],
        benchmark_duration_seconds: int,
        record_data_dir: PathType,
        **kwargs,
    ) -> RecordResult:
        print(command_output)
        size = float(re.findall(r"([\d.]+) *", command_output)[0])
        result = {
            "filesize": size,
        }

        return result

    def get_build_var_names(self) -> List[str]:
        return [
            "language",
            "src_filename",
        ]

    def get_run_var_names(self) -> List[str]:
        return [
            "master_thread_core",
        ]
