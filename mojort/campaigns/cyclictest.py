#!/usr/bin/env python3

import os
import pathlib
import random
import re
from pathlib import Path
from typing import Any, Dict, List
from deps.pythainer.src.pythainer.runners import ConcreteDockerRunner, DockerRunner
import numpy as np
from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner

import pandas as pd

from benchkit.benchmark import Benchmark, RecordResult
from benchkit.campaign import CampaignCartesianProduct
from benchkit.platforms import Platform
from benchkit.shell.shellasync import AsyncProcess
from benchkit.utils.dir import gitmainrootdir
from benchkit.utils.types import PathType

SAMPLESIZE = 100_000
DATASETREDUCTION = 0.95

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

        if language.startswith("c"):
            language_folder = "rt-tests"
        else:
            language_folder = language

        lg_bench_dir = self._benchmark_dir / language_folder
        if not self.platform.comm.isdir(path=lg_bench_dir):
            raise ValueError(
                f"Language '{language_folder}' not found as '{lg_bench_dir}' is not a directory"
            )

        match language:
            case "mojo":
                mojo_bin = "/home/user/.mojort/.venv/bin"
                cmd = f"{mojo_bin}/mojo build -O 0 -o {src_filename} {src_filename}.mojo"
            case "c":
                cmd = f"make {src_filename}"
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
        threads,
        **kwargs,
    ) -> str | AsyncProcess:
        language: str = build_variables["language"]

        if language.startswith("c"):
            language_folder = "rt-tests"
        else:
            language_folder = language

        src_filename: str = build_variables["src_filename"]
        lg_bench_dir = self._benchmark_dir / language_folder
        if language.startswith("c"):
            cmd = ["sudo", f"./{src_filename}", "--nsecs", "-vn", "-i","100", "-p","99", "-t", f"{threads}", "--duration=1m"]
        else:
            cmd = ["sudo", "python3", f"./{src_filename}.py", f"{threads}"]

        output = self.platform.comm.shell(command=cmd, current_dir=lg_bench_dir,print_output = False)

        return output

    def parse_output_to_results(
        self,
        command_output: str,
        build_variables: Dict[str, Any],
        run_variables: Dict[str, Any],
        record_data_dir: PathType,
        **kwargs,
    ) -> RecordResult:

        # data fields
        # threadnumber - iteration counter - latency
        latency = [float(x[2]) for x in re.findall(r"\s*([\d.]+):\s*([\d.]+):\s*([\d.]+)\s*", command_output)]
        nl = latency

        # sort and remove top part for outliers
        nl.sort()
        leng = len(nl)
        reduced = nl[:int(leng*DATASETREDUCTION)]

        # sample the result such that the plotting can keep up
        sampled = random.sample(reduced,SAMPLESIZE)

        # save data in seperate file
        complete_name = os.path.join(record_data_dir, build_variables["language"]+str(run_variables['threads'])+".txt")
        with open(complete_name,"w+") as f:
            for x in sampled:
                f.write(f'{str(x)}\n')
        result = {
            'datapath':complete_name,
        }

        return result

    def get_build_var_names(self) -> List[str]:
        return [
            "language",
            "src_filename",
        ]

    def get_run_var_names(self) -> List[str]:
        return [
            "threads"
        ]


def main() -> None:
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="cyclictest",
        benchmark=ProgramCompareBench(platform=platform),
        nb_runs=1,
        variables={
            "language": ["mojo","c"],
            "src_filename": ["cyclictest"],
            "threads":[1,2,3,4,],
        },
        constants={},
        debug=False,
        gdb=False,
        enable_data_dir=True,
    )
    campaign.run()

    def load_data(dataframe):
        frames = []
        for lan in dataframe["language"].unique():
            landf = dataframe[dataframe.language == lan]
            for threadcount in dataframe["threads"]:
                thrdf = landf[dataframe.threads == threadcount]
                path = thrdf.iloc[0]["datapath"]
                with open(path,"r") as f:
                    l = []
                    for line in f:
                        l.append({"language":lan,"latency":float(line),"threads":int(threadcount)})
                    frames.append(pd.DataFrame(l))
        return pd.concat(frames)

    campaign.generate_graph(
        process_dataframe=load_data,
        plot_name="catplot",
        title="comparison between latency of c and mojo for cyclictest",
        kind="violin",
        y="latency",
        x="threads",
        hue="language",
        split=True,
        inner="quart",
        height=8.27,
        aspect=15/8.27,
    )

if __name__ == "__main__":
    main()
