#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/run_tests.sh
# single: ./scripts/run_tests.sh tests/scenario_tests/test_app.py

script_dir=`dirname $0`
cd ${script_dir}/..

python setup.py install && \
  pip install "black==19.10b0" && \
  black slack_bolt/ tests/ && \
  pytest $1
