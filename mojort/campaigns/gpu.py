#!/usr/bin/env python3

import numpy as np
from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner, get_mojort_builder
from pythainer.examples.runners import gpu_runner
from benchkit.campaign import CampaignCartesianProduct
from mojort.benchmarks.matmul_gpu import MatmulGpu


CHART_ENABLED = False


def main() -> None:
    get_mojort_builder().build()
    runner = get_mojort_runner()
    runner |= gpu_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="01_gpu",
        benchmark=MatmulGpu(platform=platform),
        nb_runs=30,
        variables={
            "size": [256, 512],
            "language": [
                "mojo"
            ],
            "src_filename": ["matmul_gpu","matmul"],
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

    if not CHART_ENABLED:
        return

    def test1(dataframe):
        for lan in dataframe["src_filename"].unique():
            mojodf = dataframe[dataframe.src_filename == lan]
            avg = np.average(mojodf['runtime'])
            nw = (dataframe[dataframe.src_filename == lan]['runtime'] / avg) - 1
            dataframe.loc[dataframe["src_filename"] == lan,'normalized'] = nw
        print(dataframe)
        return dataframe

    def test2(dataframe):
        for lan in dataframe["src_filename"].unique():
            mojodf = dataframe[dataframe.src_filename == lan]
            avg = np.average(mojodf['runtime'])
            nw = (dataframe[dataframe.src_filename == lan]['runtime'] - avg)
            dataframe.loc[dataframe["src_filename"] == lan,'normalized'] = nw
        print(dataframe)
        return dataframe


    campaign.generate_graph(
        process_dataframe=test1,
        plot_name="catplot",
        title="difference between average runtime for mandelbrot program",
        kind="violin",
        ylabel='between average en actual runtime',
        y="normalized",
        # col="language",
        hue="src_filename",
        # split=True,
        inner="quart"
    )

    campaign.generate_graph(
        process_dataframe=test2,
        plot_name="catplot",
        title="difference between average runtime for mandelbrot program",
        kind="violin",
        ylabel='between average en actual runtime',
        y="normalized",
        # col="language",
        hue="src_filename",
        # split=True,
        inner="quart"
    )


    campaign.generate_graph(
        plot_name="barplot",
        x="src_filename",
        y="runtime",
    )


if __name__ == "__main__":
    main()
