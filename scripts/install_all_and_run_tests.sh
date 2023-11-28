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
python_version=`python --version | awk '{print $2}'`

if [ ${python_version:0:3} == "3.6" ]
then
  pip install -r requirements.txt
else
  pip install -e .
fi

if [[ $test_target != "" ]]
then
    pip install -r requirements/testing.txt && \
    pip install -r requirements/adapter.txt && \
    pip install -r requirements/adapter_testing.txt && \
    # To avoid errors due to the old versions of click forced by Chalice
    pip install -U pip click && \
    black slack_bolt/ tests/ && \
    pytest $1
else
    pip install -r requirements/testing.txt && \
    pip install -r requirements/adapter.txt && \
    pip install -r requirements/adapter_testing.txt && \
    # To avoid errors due to the old versions of click forced by Chalice
    pip install -U pip click && \
    black slack_bolt/ tests/ && \
    pytest && \
    pip install -U pytype && \
    pytype slack_bolt/
fi
