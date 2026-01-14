#!/bin/bash
# ./scripts/lint.sh

script_dir=$(dirname $0)
cd ${script_dir}/..

if [[ "$1" != "--no-install" ]]; then
    pip install -U pip
    pip install -U -r requirements/tools.txt
fi

flake8 slack_bolt/ && flake8 examples/
