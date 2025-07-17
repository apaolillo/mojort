#!/bin/sh
set -e

./deps/benchkit/scripts/install_venv.sh .venv
pip=./.venv/bin/pip3
$pip install -e ./deps/benchkit
$pip install -e ./deps/pythainer
$pip install -e .
$pip install -r requirements.txt
