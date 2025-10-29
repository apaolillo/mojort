#!/usr/bin/env python3

from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner, get_mojort_builder
from benchkit.campaign import CampaignCartesianProduct, CampaignSuite
from mojort.benchmarks.mandelbrot import MandelbrotBench
from mojort.benchmarks.matmul import MatmulBench
from mojort.benchmarks.kmp import KmpBench
from benchkit.platforms import Platform
from benchkit.commandwrappers.taskset import TasksetWrap
from benchkit.benchmark import CommandWrapper


nb_runs = 1
master_thread_core = [11]
languages = [
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
]


def mandelbrot_campaign(
    platform: Platform,
    wrappers: list[CommandWrapper],
) -> CampaignCartesianProduct:
    return CampaignCartesianProduct(
        name="11_mandelbrot",
        benchmark=MandelbrotBench(
            command_wrappers=wrappers,
            platform=platform,
        ),
        nb_runs=nb_runs,
        variables={
            "size": [
                256,
                512,
                # 1024,
            ],
            "language": languages,
            "src_filename": ["mandelbrot"],
            "master_thread_core": master_thread_core,
        },
        constants={},
        debug=False,
        gdb=False,
        enable_data_dir=True,
        continuing=False,
    )


def matmul_campaign(
    platform: Platform,
    wrappers: list[CommandWrapper],
) -> CampaignCartesianProduct:
    return CampaignCartesianProduct(
        name="12_matmul",
        benchmark=MatmulBench(
            command_wrappers=wrappers,
            platform=platform,
        ),
        nb_runs=nb_runs,
        variables={
            "size": [
                256,
                512,
                # 1024,
            ],
            "language": languages,
            "src_filename": ["matmul"],
            "master_thread_core": master_thread_core,
        },
        constants={},
        debug=False,
        gdb=False,
        enable_data_dir=True,
        continuing=False,
    )

def kmp_campaign(
    platform: Platform,
    wrappers: list[CommandWrapper],
) -> CampaignCartesianProduct:
    return CampaignCartesianProduct(
        name="13_kmp",
        benchmark=KmpBench(
            command_wrappers=wrappers,
            platform=platform,
        ),
        nb_runs=nb_runs,
        variables={
            "size": [
                0.2,
                0.5,
                # 1.0,
            ],
            "language": languages,
            "src_filename": ["knmp"],
            "master_thread_core": master_thread_core,
        },
        constants={},
        debug=False,
        gdb=False,
        enable_data_dir=True,
        continuing=False,
    )


def main() -> None:
    get_mojort_builder().build()
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    taskset = TasksetWrap()

    def campaign(
        campaign_function,
    ) -> CampaignCartesianProduct:
        return campaign_function(
            platform=platform,
            wrappers=[
                taskset,
            ]
        )

    campaigns = [
        campaign(kmp_campaign),
        campaign(matmul_campaign),
        campaign(mandelbrot_campaign),
    ]

    suite = CampaignSuite(campaigns=campaigns)
    suite.print_durations()
    suite.run_suite()


if __name__ == "__main__":
    main()
