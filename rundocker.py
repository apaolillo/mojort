#!/usr/bin/env python3

from mojort.runners import get_mojort_builder, get_mojort_runner
from benchkit.utils.dir import gitmainrootdir
from pathlib import Path
from pythainer.runners import DockerRunner


def buildrun(
    batch: bool,
) -> None:
    docker_builder = get_mojort_builder()
    docker_builder.build()

    docker_runner = get_mojort_runner()

    cmd = docker_runner.get_command()
    print(" ".join(cmd))

    docker_runner.generate_script()

    if not batch:
        docker_runner.run()


def main() -> None:
    buildrun(batch=False)


if __name__ == "__main__":
    main()
