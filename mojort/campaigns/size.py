#!/usr/bin/env python3

from benchkit.campaign import CampaignCartesianProduct

from mojort.benchmarks.size import SizeBench
from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner


def main() -> None:
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="size",
        benchmark=SizeBench(platform=platform),
        nb_runs=1,
        variables={
            "language": [
                "cpp-gcc",
                "cpp-clang",
                "c-gcc",
                "c-clang",
                "rust",
                "mojo",
            ],
            "opt_level": [
                "O0",
                "O3",
            ],
            "src_filename": ["knmp", "matmul", "mandelbrot"],
        },
        constants={},
        debug=False,
        gdb=False,
        enable_data_dir=True,
    )

    campaign.run()

    campaign.generate_graph(
        plot_name="catplot",
        row="src_filename",
        kind="bar",
        orient="h",
        x="filesize",
        y="language",
        hue="opt_level",
    )


if __name__ == "__main__":
    main()
