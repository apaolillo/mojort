#!/usr/bin/env python3

from mojort.platforms import get_mojort_docker_platform_from
from mojort.runners import get_mojort_runner, get_mojort_builder
from benchkit.campaign import CampaignCartesianProduct
from mojort.benchmarks.microbench import MicrobenchBench


def main() -> None:
    get_mojort_builder().build()
    runner = get_mojort_runner()
    platform = get_mojort_docker_platform_from(runner=runner)
    campaign = CampaignCartesianProduct(
        name="matmul",
        benchmark=MicrobenchBench([],platform=platform),
        nb_runs=20,
        variables={
            "size": [16, 32],
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
            "src_filename": ["matmul"],
            # "size": [512,1024,2048],
            #"size": [512,],
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

    """
    def test(dataframe):
        dataframe = dataframe[dataframe['size'] == 512]
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
    """

    campaign.generate_graph(
        plot_name="barplot",
        x="size",
        y="runtime",
        hue="language",
    )
    """
    campaign.generate_graph(
        plot_name="barplot",
        x="language",
        y="filesize",
    )
    """


if __name__ == "__main__":
    main()
