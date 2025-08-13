# mojort

Howto:

```bash
git clone git@gitlab.soft.vub.ac.be:perfsys/papers/mojort.git
cd mojort/
git submodule update --init --recursive
./configure.sh
. ./.venv/bin/activate
cd mojort/campaigns/
./latencytest.py
```

## Requirements

### Docker

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Reboot
```

### Install the NVIDIA Container Toolkit

See instructions on [NVIDIA's website](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).


## Run examples

### Run the GPU example

Example is taken from the [Mojo tutorial](https://docs.modular.com/mojo/manual/gpu/intro-tutorial/).

```bash
. ./.venv/bin/activate
./rundocker.py
cd ~/workspace/mojort/benchmarks/mojo/
. ~/.mojort/.venv/bin/activate
mojo gpu_vecadd.mojo
```
