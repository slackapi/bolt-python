#!/bin/bash
# ./scripts/run_flake8.sh

script_dir=$(dirname $0)
cd ${script_dir}/.. && \
  pip install -U -r requirements/tools.txt && \
  flake8 slack_bolt/ && flake8 examples/
