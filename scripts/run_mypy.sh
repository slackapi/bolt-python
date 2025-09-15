#!/bin/bash
# ./scripts/run_mypy.sh

script_dir=$(dirname $0)
cd ${script_dir}/.. && \
  pip install -U .
  pip install -U -r requirements/async.txt && \
  pip install -U -r requirements/adapter.txt && \
  pip install -U -r requirements/tools.txt && \
  mypy --config-file pyproject.toml
