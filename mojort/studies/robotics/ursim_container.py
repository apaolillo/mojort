#!/usr/bin/env python3

from pythainer.runners import ConcreteDockerRunner


def ursim_runner(robot_model: str = "UR10") -> ConcreteDockerRunner:
    if robot_model not in ["UR3", "UR5", "UR10", "UR16", "UR20"]:
        raise ValueError(f"Invalid robot model: {robot_model}")

    docker_runner = ConcreteDockerRunner(
        image="universalrobots/ursim_e-series:5.19",
        name="ursim",
        environment_variables={"ROBOT_MODEL": robot_model},
        other_options=[
            "--publish",
            "5900:5900",
            "--publish",
            "6080:6080",
            "--publish",
            "29999:29999",
        ],
        root=True,
    )
    return docker_runner


if __name__ == "__main__":
    ursim_runner().run()
