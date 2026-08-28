#!/bin/bash
# ./scripts/lint.sh

script_dir=$(dirname $0)
cd ${script_dir}/..

if [[ "$1" != "--no-install" ]]; then
    pip install -U pip
    pip install -U -r requirements/dev_tools.txt
fi

ruff check slack_bolt/ examples/
ruff format --check slack_bolt/ tests/ examples/
