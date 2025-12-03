from pathlib import Path

from benchkit.utils.dir import gitmainrootdir
from pythainer.builders import PartialDockerBuilder, UbuntuDockerBuilder
from pythainer.examples.builders import (
    get_user_gui_builder,
    qemu_builder,
    qemu_dependencies,
    rust_builder,
)
from pythainer.runners import ConcreteDockerRunner
from pythainer.sysutils import PathType as PythainerPathType


def add_toyos(
    builder: PartialDockerBuilder,
) -> None:
    embedded_packages = [
        "gcc-aarch64-linux-gnu",
        "gcc-arm-none-eabi",
        "binutils-aarch64-linux-gnu",
        "gcc-aarch64-linux-gnu",
        "gdb-multiarch",
        "device-tree-compiler",
        "bsdextrautils",
        "tio",
    ]
    packages = embedded_packages + qemu_dependencies()
    builder.root()
    builder.add_packages(packages=packages)
    builder.user()
    builder |= qemu_builder(version="10.0.2", cleanup=False)


def mojo_builder(
    modular_version="25.4.0",
    nightly: bool = False,
) -> PartialDockerBuilder:
    """
    Sets up a Docker builder for Mojo development using Modular's installation instructions
    (see https://docs.modular.com/max/packages).

    Parameters:
        modular_version:
            The version of Mojo to use. Defaults to 25.4.0 (Jun 18, 2025).
        nightly (bool):
            Whether to install the nightly version of Modular/Mojo.
            Defaults to False (stable).

    Returns:
        PartialDockerBuilder: Docker builder configured for Mojo development.
    """
    builder = PartialDockerBuilder()

    # Install Python and pip if not already present
    builder.add_packages(
        packages=[
            "python3",
            "python3-full",
            "python3-venv",
            "python3-pip",
            "libnuma-dev",
        ]
    )

    mojo_config_path = "/home/${USER_NAME}/.mojort"
    venv_path = f"{mojo_config_path}/.venv"
    builder.user()
    builder.run_multiple(
        commands=[
            f"mkdir -p {mojo_config_path}",
            f"python3 -m venv {venv_path}",
            f"{venv_path}/bin/pip3 install --upgrade pip",
        ]
    )

    if nightly:
        # Nightly installation using pre-release Modular package and nightly index
        builder.run(
            f"{venv_path}/bin/pip3 install --pre modular "
            "--extra-index-url https://download.pytorch.org/whl/cpu "
            "--index-url https://dl.modular.com/public/nightly/python/simple/"
        )
    else:
        # Stable installation using the default and extra index URLs
        builder.run(
            f'{venv_path}/bin/pip3 install "modular<={modular_version}" '
            "--extra-index-url https://download.pytorch.org/whl/cpu "
            "--extra-index-url https://modular.gateway.scarf.sh/simple/"
        )

    # Validate install
    builder.run(f"{venv_path}/bin/mojo --version")

    return builder


def get_mojort_builder(
    image_name: str = "mojort",
) -> UbuntuDockerBuilder:
    builder = get_user_gui_builder(
        image_name=image_name,
        base_ubuntu_image="ubuntu:24.04",
    )
    builder.space()
    builder.desc("Install Mojo")
    builder |= mojo_builder(nightly=False)
    mojo_venv_path = "~/.mojort/.venv"
    pip3 = f"{mojo_venv_path}/bin/pip3"
    builder.run(
        command=f'echo ". {mojo_venv_path}/bin/activate" >> /home/${{USER_NAME}}/.bash_history'
    )
    builder.space()

    builder.workdir("/home/${USER_NAME}/workspace")
    add_toyos(builder=builder)

    # Install Rust
    builder.desc("Rust")
    builder |= rust_builder()

    builder.root()
    builder.add_packages(packages=["clang"])
    builder.user()

    builder.desc("Install Python packages")
    builder.run(command=f"{pip3} install --upgrade pip")
    requirements_path = gitmainrootdir() / "requirements.txt"
    requirements = sorted(line.strip() for line in requirements_path.read_text().splitlines())
    requirements_str = " ".join(requirements)
    builder.run(command=f"{pip3} install --upgrade {requirements_str}")

    builder.workdir("/home/${USER_NAME}")
    builder.space()

    return builder


def get_mojort_runner(
    workdir: PythainerPathType = "/home/user",
    image_name: str = "mojort",
) -> ConcreteDockerRunner:
    repo_dir = gitmainrootdir().resolve()
    docker_path = Path("/home/user/workspace/mojort/")

    runner = ConcreteDockerRunner(
        image=image_name,
        environment_variables={},
        volumes={f"{repo_dir}": f"{docker_path}"},
        devices=[],
        other_options=["--privileged"],
        network="host",
        workdir=workdir,
    )
    # runner |= gpu_runner()
    # runner |= gui_runner()
    # runner |= personal_runner()

    return runner
