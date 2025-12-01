from benchkit.communication.docker import DockerCommLayer
from benchkit.platforms import Platform
from pythainer.runners import ConcreteDockerRunner


def get_mojort_docker_platform_from(
    runner: ConcreteDockerRunner,
) -> Platform:
    comm = DockerCommLayer(docker_runner=runner)
    platform = Platform(comm_layer=comm)
    return platform
