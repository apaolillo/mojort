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
