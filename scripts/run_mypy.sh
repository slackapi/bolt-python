#!/bin/bash
# ./scripts/run_mypy.sh

script_dir=$(dirname $0)
cd ${script_dir}/.. && \
  pip install .
  pip install -r requirements/async.txt && \
  pip install -r requirements/adapter.txt && \
  pip install -r requirements/tools.txt && \
  mypy slack_bolt/
