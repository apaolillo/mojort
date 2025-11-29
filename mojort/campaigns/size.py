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
                # --- C++ GCC
                "cpp-gcc",
                "cpp-gcc -O3",
                # --- C++ Clang
                "cpp-clang",
                "cpp-clang -O3",
                # "cpp -Ofast",
                # --- C GCC
                "c-gcc",
                "c-gcc -O3",
                # --- C Clang
                "c-clang",
                "c-clang -O3",
                # --- Rust
                "rust",
                "rust -O3",
                # --- Mojo
                "mojo",
                "mojo -O3",
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
    )


if __name__ == "__main__":
    main()
