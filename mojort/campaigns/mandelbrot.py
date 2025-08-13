#!/usr/bin/env python3

import pathlib
import re
from pathlib import Path
from typing import Any, Dict, List
import numpy as np
from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner, get_mojort_builder

import pandas as pd

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

    @staticmethod
    def _language2foldername(language: str) -> str:
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

    def build_bench(
        self,
        language: str,
        src_filename: str,
        **kwargs,
    ) -> None:
        language_folder = self._language2foldername(language)

        lg_bench_dir = self._benchmark_dir / language_folder
        if not self.platform.comm.isdir(path=lg_bench_dir):
            raise ValueError(
                f"Language '{language_folder}' not found as '{lg_bench_dir}' is not a directory"
            )

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
                cmd = f"rustc -C opt-level=3 {src_filename}.rs -o {src_filename}"
            case "rust -O2":
                cmd = f"rustc -C opt-level=2 {src_filename}.rs -o {src_filename}"
            case "rust -O1":
                cmd = f"rustc -C opt-level=1 {src_filename}.rs -o {src_filename}"
            case "rust":
                cmd = f"rustc {src_filename}.rs -o {src_filename}"

            # --- Mojo
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
        size,
        **kwargs,
    ) -> str | AsyncProcess:
        language: str = build_variables["language"]
        language_folder = self._language2foldername(language)

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


        language: str = build_variables["language"]
        language_folder = self._language2foldername(language)

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
            "size"
        ]


def main() -> None:
    get_mojort_builder().build()
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="01_latency",
        benchmark=ProgramCompareBench(platform=platform),
        nb_runs=20,
        variables={
            "size": [128, 512],
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
            "src_filename": ["mandelbrot"],
            #"size": [ x * 512 for x in range(1,11)],
            #"size": [512, 1024, 2048],
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

    def test(dataframe):
        sizes=dataframe["size"].unique()
        sizes.sort()
        dataframe = dataframe[dataframe['size'] == sizes[-1]]
        for lan in dataframe["language"].unique():
            mojodf = dataframe[dataframe.language == lan]
            avg = np.average(mojodf['runtime'])
            nw = (dataframe[dataframe.language == lan]['runtime'] / avg) - 1
            dataframe.loc[dataframe["language"] == lan,'normalized'] = nw
        print(dataframe)
        return dataframe


    def speedup(dataframe):
        sizes=dataframe["size"].unique()
        sizes.sort()
        frames = []
        print("---------------------")
        for lan in dataframe["language"].unique():
            dataframemin = dataframe[dataframe['size'] == sizes[0]]
            ref = sizes[0] * sizes[0]
            mojodf = dataframemin[dataframemin.language == lan]
            avg_min = np.average(mojodf['runtime'])
            landf = dataframe[dataframe.language == lan]

            for size in dataframe["size"].unique():
                r = avg_min * ((size * size)/ref)
                runtimes = landf[landf['size'] == size]["runtime"]/r
                landf.loc[(landf["language"] == lan) & (landf['size'] == size),'computation_per_element'] = runtimes
                frames.append(landf)
        a = pd.concat(frames)
        print(a)
        b = a.dropna()
        return b

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
        x="size",
        y="runtime",
        hue="language",
    )

    campaign.generate_graph(
        process_dataframe=speedup,
        plot_name="lineplot",
        x="size",
        hue="language",
        y="computation_per_element",
    )

    campaign.generate_graph(
        plot_name="barplot",
        x="language",
        y="filesize",
    )


if __name__ == "__main__":
    main()
