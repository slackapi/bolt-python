#!/bin/bash
# ./scripts/run_pytype.sh

script_dir=$(dirname $0)
cd ${script_dir}/.. && \
  pip install .
  pip install -r requirements/async.txt && \
  pip install -r requirements/adapter.txt && \
  pip install "pytype==2022.12.15" && \
  pytype slack_bolt/
