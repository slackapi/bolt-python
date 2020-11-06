#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/install_all_and_run_tests.sh
# single: ./scripts/install_all_and_run_tests.sh tests/scenario_tests/test_app.py

script_dir=`dirname $0`
cd ${script_dir}/..
rm -rf ./slack_bolt.egg-info
# The package causes a conflict with moto
pip uninstall python-lambda

test_target="$1"

if [[ $test_target != "" ]]
then
  pip install -e ".[testing]" && \
    pip install -e ".[adapter]" && \
    black slack_bolt/ tests/ && \
    pytest $1
else
  pip install -e ".[testing]" && \
    pip install -e ".[adapter]" && \
    black slack_bolt/ tests/ && \
    pytest && \
    pip install -U pytype && \
    pytype slack_bolt/
fi
