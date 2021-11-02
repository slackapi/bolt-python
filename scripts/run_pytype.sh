#!/bin/bash
# ./scripts/run_pytype.sh

script_dir=$(dirname $0)
cd ${script_dir}/.. && \
  pip install -e ".[async]" && \
  pip install -e ".[adapter]" && \
  pip install "pytype==2021.10.25" && \
  pytype slack_bolt/
