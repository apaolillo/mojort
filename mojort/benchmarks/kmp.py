import re
from pathlib import Path
from typing import Any, Dict, List
from mojort.utils import language2cmdline, language2foldername
from benchkit.benchmark import Benchmark, RecordResult
from benchkit.platforms import Platform
from benchkit.utils.dir import gitmainrootdir
from benchkit.utils.types import PathType


class KmpBench(Benchmark):
    def __init__(self, platform: Platform):
        super().__init__(
            command_wrappers=(),
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
        **kwargs,
    ) -> str:

        language: str = build_variables["language"]
        language_folder = language2foldername(language)

        src_filename: str = build_variables["src_filename"]
        lg_bench_dir = self._benchmark_dir / language_folder
        cmd = [f"./{src_filename}",]

        output = self.platform.comm.shell(command=cmd, current_dir=lg_bench_dir)

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
        #language: str = build_variables["language"]
        #language_folder = language2foldername(language)

        # src_filename: str = build_variables["src_filename"]
        # lg_bench_dir = self._benchmark_dir / language_folder
        # cmd = ["du",f"{src_filename}",]
        # output = self.platform.comm.shell(command=cmd, current_dir=lg_bench_dir)
        # size = [float(m) for m in re.findall(r"([\d.]+) *", output)][0]
        result = {
            # "filesize": size,
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
        ]
