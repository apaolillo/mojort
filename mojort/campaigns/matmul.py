#!/usr/bin/env python3

import pathlib
import re
from pathlib import Path
from typing import Any, Dict, List
from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner, get_mojort_builder
from mojort.utils import language2foldername, language2cmdline

from benchkit.benchmark import Benchmark, RecordResult
from benchkit.campaign import CampaignCartesianProduct
from benchkit.platforms import Platform
from benchkit.shell.shellasync import AsyncProcess
from benchkit.utils.dir import gitmainrootdir
from benchkit.utils.types import PathType


class ProgramCompareBench(Benchmark):
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
    def bench_src_path(self) -> pathlib.Path:
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
        size,
        **kwargs,
    ) -> str | AsyncProcess:
        language: str = build_variables["language"]
        language_folder = language2foldername(language)

        src_filename: str = build_variables["src_filename"]
        lg_bench_dir = self._benchmark_dir / language_folder
        cmd = [f"./{src_filename}",f'{size}']

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

        #src_filename: str = build_variables["src_filename"]
        #lg_bench_dir = self._benchmark_dir / language_folder
        #cmd = ["du",f"{src_filename}",]
        #output = self.platform.comm.shell(command=cmd, current_dir=lg_bench_dir)
        #size = [float(m) for m in re.findall(r"([\d.]+) *", output)][0]
        result = {
            #"filesize": size,
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
            "size"
        ]


def main() -> None:
    get_mojort_builder().build()
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="matmul",
        benchmark=ProgramCompareBench(platform=platform),
        nb_runs=20,
        variables={
            "size": [16, 32],
            "language": [
                # --- C++ GCC
                "cpp-gcc", "cpp-gcc -O1", "cpp-gcc -O2", "cpp-gcc -O3",
                # --- C++ Clang
                "cpp-clang", "cpp-clang -O1", "cpp-clang -O2", "cpp-clang -O3",
                #"cpp -Ofast",

                # --- C GCC
                "c-gcc", "c-gcc -O1", "c-gcc -O2", "c-gcc -O3",
                # --- C Clang
                "c-clang", "c-clang -O1", "c-clang -O2", "c-clang -O3",

                # --- Rust
                "rust", "rust -O1", "rust -O2", "rust -O3",

                # --- Mojo
                "mojo", "mojo -O1", "mojo -O2", "mojo -O3",
            ],
            "src_filename": ["matmul"],
            # "size": [512,1024,2048],
            #"size": [512,],
        },
        constants={},
        debug=False,
        gdb=False,
        enable_data_dir=True,
        continuing=False,
    )
    campaign.run()

    # NOTE: there are mistakes made by one of the langaues as both do not produce the exact same output
    # this might be worth mentioning in the paper

    """
    def test(dataframe):
        dataframe = dataframe[dataframe['size'] == 512]
        for lan in dataframe["language"].unique():
            mojodf = dataframe[dataframe.language == lan]
            avg = np.average(mojodf['runtime'])
            nw = (dataframe[dataframe.language == lan]['runtime'] / avg) - 0
            dataframe.loc[dataframe["language"] == lan,'normalized'] = nw
        print(dataframe)
        return dataframe

    campaign.generate_graph(
        process_dataframe=test,
        plot_name="catplot",
        title="difference between average runtime for mandelbrot program",
        kind="violin",
        ylabel='between average en actual runtime',
        y="normalized",
        # col="language",
        hue="language",
        # split=True,
        inner="quart"
    )
    """

    campaign.generate_graph(
        plot_name="barplot",
        x="size",
        y="runtime",
        hue="language",
    )
    """
    campaign.generate_graph(
        plot_name="barplot",
        x="language",
        y="filesize",
    )
    """


if __name__ == "__main__":
    main()
