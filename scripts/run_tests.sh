#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/run_tests.sh
# single: ./scripts/run_tests.sh tests/scenario_tests/test_app.py

script_dir=`dirname $0`
cd ${script_dir}/..

test_target="$1"
python_version=`python --version | awk '{print $2}'`

if [[ $test_target != "" ]]
then
  black slack_bolt/ tests/ && \
    pytest -vv $1
else
  if [ ${python_version:0:3} == "3.8" ]
  then
    # pytype's behavior can be different in older Python versions
    black slack_bolt/ tests/ \
      && pytest -vv \
      && pip install -r requirements/adapter.txt \
      && pip install -r requirements/adapter_testing.txt \
      && pip install -U pip setuptools wheel \
      && pip install -U pytype \
      && pytype slack_bolt/
  else
    black slack_bolt/ tests/ && pytest
  fi
fi
