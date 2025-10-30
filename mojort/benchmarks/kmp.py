import re
from pathlib import Path
from typing import Any, Dict, List, Iterable
from mojort.utils import language2cmdline, language2foldername, rust_add_build_path, rust_add_executable_path
from benchkit.benchmark import Benchmark, RecordResult, CommandWrapper
from benchkit.platforms import Platform
from benchkit.utils.dir import gitmainrootdir
from benchkit.utils.types import PathType


class KmpBench(Benchmark):
    def __init__(
        self,
        command_wrappers: Iterable[CommandWrapper],
        platform: Platform,
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

        cmd = language2cmdline(language=language, src_filename=src_filename)

        self.platform.comm.shell(
            command=cmd,
            current_dir=lg_bench_dir,
            output_is_log=True,
        )

    def single_run(
        self,
        build_variables: Dict[str, Any],
        size,
        **kwargs,
    ) -> str:

        language: str = build_variables["language"]
        language_folder = language2foldername(language)

        src_filename: str = build_variables["src_filename"]
        lg_bench_dir = self._benchmark_dir / language_folder
        lg_bench_dir = rust_add_executable_path(language,src_filename,lg_bench_dir)
        cmd = [f"./{src_filename}",f"{size}"]

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

        runtime = [float(m) for m in re.findall(r"runtime: ([\d.]+) µs", command_output)][0]

        result = {
            "runtime": runtime,
        }

        return result

    def get_build_var_names(self) -> List[str]:
        return [
            "language",
            "src_filename",
        ]

    def get_run_var_names(self) -> List[str]:
        return [
            "size",
            "master_thread_core",
        ]
