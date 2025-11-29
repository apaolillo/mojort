import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

from benchkit.benchmark import Benchmark, CommandWrapper, RecordResult
from benchkit.platforms import Platform
from benchkit.utils.dir import gitmainrootdir
from benchkit.utils.types import PathType

from mojort.utils import get_object_build_command, language2foldername


class SizeBench(Benchmark):
    def __init__(
        self,
        platform: Platform,
        command_wrappers: Iterable[CommandWrapper] = (),
    ) -> None:
        super().__init__(
            command_wrappers=command_wrappers,
            command_attachments=(),
            shared_libs=(),
            pre_run_hooks=(),
            post_run_hooks=(),
        )
        self.platform = platform
        gmrd_host = gitmainrootdir()
        gmrd = self.platform.comm.host_to_comm_path(host_path=gmrd_host)
        self._src_path = gmrd / "benchmarks"

    @property
    def bench_src_path(self) -> Path:
        return self._src_path

    def build_bench(
        self,
        language: str,
        opt_level: str,
        src_filename: str,
        **kwargs,
    ) -> None:
        cmd = get_object_build_command(
            language=language,
            opt_level=opt_level,
            src_filename=src_filename,
        )

        language_folder = language2foldername(language)
        if language.startswith("rust"):
            language_folder = Path(language_folder) / src_filename

        lg_bench_dir = self._src_path / language_folder
        if not self.platform.comm.isdir(path=lg_bench_dir):
            raise ValueError(
                f"Language '{language_folder}' not found as '{lg_bench_dir}' is not a directory"
            )

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

        src_filename: str = build_variables["src_filename"]
        lg_bench_dir = self._src_path / language2foldername(language)
        if language.startswith("rust"):
            lg_bench_dir = Path(lg_bench_dir) / src_filename

        # Command to analyze the file size
        cmd = ["du", "-b", f"./{src_filename}.o"]

        # Strip the file
        self.platform.comm.shell(f"strip -s ./{src_filename}.o", current_dir=lg_bench_dir)

        # Command to get the object dump for debugging
        self.platform.comm.shell(
            command=f"objdump -d ./{src_filename}.o > ./{src_filename}.dmp",
            shell=True,
            current_dir=lg_bench_dir,
        )

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
            "opt_level",
            "src_filename",
        ]

    def get_run_var_names(self) -> List[str]:
        return [
            "master_thread_core",
        ]
