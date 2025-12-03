#!/usr/bin/env python3

from benchkit.benchmark import CommandWrapper
from benchkit.campaign import CampaignCartesianProduct, CampaignSuite
from benchkit.commandwrappers.taskset import TasksetWrap
from benchkit.platforms import Platform

from mojort.benchmarks.microbench import MicrobenchBench
from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_builder, get_mojort_runner

nb_runs = 20
master_thread_core = [11]

# Separate language and optimization level variables
languages = [
    "cpp-gcc",
    "cpp-clang",
    "c-gcc",
    "c-clang",
    "rust",
    "mojo",
]

opt_levels = [
    "O0",
    "O1",
    "O2",
    "O3",
]


def mandelbrot_campaign(
    platform: Platform,
    wrappers: list[CommandWrapper],
) -> CampaignCartesianProduct:
    return CampaignCartesianProduct(
        name="11_mandelbrot",
        benchmark=MicrobenchBench(
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
            "opt_level": opt_levels,
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
        benchmark=MicrobenchBench(
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
            "opt_level": opt_levels,
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
        benchmark=MicrobenchBench(
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
            "opt_level": opt_levels,
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
            ],
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
