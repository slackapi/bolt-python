#!/bin/bash
# ./scripts/run_pytype.sh

script_dir=$(dirname $0)
cd ${script_dir}/.. && \
  pip install -e ".[adapter]" && \
  pip install -U pytype && \
  pytype slack_bolt/
