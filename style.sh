#!/bin/sh
set -e

venv="./.venv/bin/"
flake8="${venv}/flake8"
isort="${venv}/isort"
black="${venv}/black"

${isort} --profile=black mojort/ notebooks/
${black} .
#${flake8} --profile=black mojort/ notebooks/
