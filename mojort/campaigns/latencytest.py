#!/usr/bin/env python3

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


class LatencyBench(Benchmark):
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
        lg_bench_dir = self._benchmark_dir / language

        if not self.platform.comm.isdir(path=lg_bench_dir):
            raise ValueError(
                f"Language '{language}' not found as '{lg_bench_dir}' is not a directory"
            )

        match language:
            case "c":
                cmd = f"gcc -O3 -o {src_filename} {src_filename}.c"
            case "mojo":
                mojo_bin = "/home/user/.mojort/.venv/bin"
                cmd = f"{mojo_bin}/mojo build -o {src_filename} {src_filename}.mojo"
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
        src_filename: str = build_variables["src_filename"]
        lg_bench_dir = self._benchmark_dir / language
        cmd = [f"./{src_filename}"]

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
        latencies = [float(m) for m in re.findall(r"Latency = ([\d.]+) µs", command_output)]
        total_match = re.search(r"Total latency: ([\d.]+) µs", command_output)
        total_latency = float(total_match.group(1)) if total_match else None
        latencies_np = np.array(latencies) if latencies else np.array([0.0])

        result = {
            "latency_min": float(np.min(latencies_np)),
            "latency_max": float(np.max(latencies_np)),
            "latency_median": float(np.median(latencies_np)),
            "latency_mean": float(np.mean(latencies_np)),
            "latency_std": float(np.std(latencies_np, ddof=1)),  # sample stddev
            "latency_sum": float(np.sum(latencies_np)),
            "total_latency": total_latency,
        }

        return result

    def get_build_var_names(self) -> List[str]:
        return [
            "language",
            "src_filename",
        ]

    def get_run_var_names(self) -> List[str]:
        return []


def main() -> None:
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="01_latency",
        benchmark=LatencyBench(platform=platform),
        nb_runs=50,
        variables={
            "language": ["c", "mojo"],
            "src_filename": ["sleep_interval"],
        },
        constants={},
        debug=False,
        gdb=False,
        enable_data_dir=True,
    )
    campaign.run()
    campaign.generate_graph(
        plot_name="catplot",
        title="Naive Latency Test",
        kind="strip",
        y="total_latency",
        col="language",
        hue="language",
    )


if __name__ == "__main__":
    main()
