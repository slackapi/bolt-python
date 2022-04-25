#!/bin/bash
# ./scripts/run_flake8.sh

script_dir=$(dirname $0)
cd ${script_dir}/.. && \
  pip install "flake8==4.0.1" && \
  flake8 slack_bolt/ && flake8 examples/
