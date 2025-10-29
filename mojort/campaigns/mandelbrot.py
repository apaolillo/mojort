#!/usr/bin/env python3

import numpy as np
from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner, get_mojort_builder
import pandas as pd
from benchkit.campaign import CampaignCartesianProduct
from mojort.benchmarks.mandelbrot import MandelbrotBench


def main() -> None:
    get_mojort_builder().build()
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="01_latency",
        benchmark=MandelbrotBench([],platform=platform),
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
