#!/bin/bash
# ./scripts/run_pytype.sh

script_dir=$(dirname $0)
cd ${script_dir}/.. && \
  pip install -e ".[adapter]" && \
  # TODO: upgrade pytype
  pip install "pytype==2021.9.27" && \
  pytype slack_bolt/
