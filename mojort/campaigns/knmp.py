#!/usr/bin/env python3

import os
import pathlib
import re
from pathlib import Path
from typing import Any, Dict, List
import numpy as np
from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner

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

        # -O flags are modeled as a seperate language but the folder is still the same
        if language.startswith("cpp"):
            language_folder = "cpp"
        elif language.startswith("mojo"):
            language_folder = "mojo"
        else:
            language_folder = language

        lg_bench_dir = self._benchmark_dir / language_folder
        if not self.platform.comm.isdir(path=lg_bench_dir):
            raise ValueError(
                f"Language '{language_folder}' not found as '{lg_bench_dir}' is not a directory"
            )

        match language:
            case "cpp -O3":
                cmd = f"g++ -O3 {src_filename}.cpp -o {src_filename}"
            case "cpp -O2":
                cmd = f"g++ -O2 {src_filename}.cpp -o {src_filename}"
            case "cpp -O1":
                cmd = f"g++ -O1 {src_filename}.cpp -o {src_filename}"
            case "cpp":
                cmd = f"g++ {src_filename}.cpp -o {src_filename}"
            case "mojo":
                mojo_bin = "/home/user/.mojort/.venv/bin"
                cmd = f"{mojo_bin}/mojo build -O 0 -o {src_filename} {src_filename}.mojo"
            case "mojo -O1":
                mojo_bin = "/home/user/.mojort/.venv/bin"
                cmd = f"{mojo_bin}/mojo build -O 1 -o {src_filename} {src_filename}.mojo"
            case "mojo -O2":
                mojo_bin = "/home/user/.mojort/.venv/bin"
                cmd = f"{mojo_bin}/mojo build -O 2 -o {src_filename} {src_filename}.mojo"
            case "mojo -O3":
                mojo_bin = "/home/user/.mojort/.venv/bin"
                cmd = f"{mojo_bin}/mojo build -O 3 -o {src_filename} {src_filename}.mojo"
            case _:
                raise ValueError(f"Unknown language '{language}'")

        self.platform.comm.shell(
            command=cmd,
            current_dir=lg_bench_dir,
            output_is_log=True,
        )

    def single_run(
        self,
        build_variables: Dict[str, Any],
        **kwargs,
    ) -> str | AsyncProcess:
        language: str = build_variables["language"]

        # -O flags are modeled as a seperate language but the folder is still the same
        if language.startswith("cpp"):
            language_folder = "cpp"
        elif language.startswith("mojo"):
            language_folder = "mojo"
        else:
            language_folder = language

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


        language: str = build_variables["language"]
        if language.startswith("cpp"):
            language_folder = "cpp"
        elif language.startswith("mojo"):
            language_folder = "mojo"
        else:
            language_folder = language

        src_filename: str = build_variables["src_filename"]
        lg_bench_dir = self._benchmark_dir / language_folder
        cmd = ["du",f"{src_filename}",]
        output = self.platform.comm.shell(command=cmd, current_dir=lg_bench_dir)
        size = [float(m) for m in re.findall(r"([\d.]+) *", output)][0]
        result = {
            "filesize": size,
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


def main() -> None:
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="knmp",
        benchmark=ProgramCompareBench(platform=platform),
        nb_runs=20,
        variables={
            "language": ["cpp","cpp -O1","cpp -O2","cpp -O3","mojo","mojo -O1","mojo -O2","mojo -O3",],
            "src_filename": ["knmp"],
        },
        constants={},
        debug=False,
        gdb=False,
        enable_data_dir=True,
    )
    campaign.run()
    def test(dataframe):
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



    campaign.generate_graph(
        plot_name="barplot",
        x="language",
        y="runtime",
    )
    campaign.generate_graph(
        plot_name="barplot",
        x="language",
        y="filesize",
    )


if __name__ == "__main__":
    main()
