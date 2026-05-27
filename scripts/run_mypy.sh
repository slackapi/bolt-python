#!/bin/bash
# ./scripts/run_mypy.sh

script_dir=$(dirname $0)
cd ${script_dir}/..

if [[ "$1" != "--no-install" ]]; then
  pip install -U pip
  pip install -U .
  pip install -U -r requirements/async_dev.txt
  pip install -U -r requirements/adapter_dev.txt
  pip install -U -r requirements/dev_tools.txt
fi

mypy --config-file pyproject.toml
