#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/install_all_and_run_tests.sh
# single: ./scripts/install_all_and_run_tests.sh tests/scenario_tests/test_app.py

script_dir=`dirname $0`
cd ${script_dir}/..
rm -rf ./slack_bolt.egg-info

# Update pip to prevent warnings
pip install -U pip

# The package causes a conflict with moto
pip uninstall python-lambda

test_target="$1"

pip install -U -e .
pip install -U -r requirements/testing.txt
pip install -U -r requirements/adapter.txt
pip install -U -r requirements/adapter_testing.txt
pip install -U -r requirements/tools.txt
# To avoid errors due to the old versions of click forced by Chalice
pip install -U pip click

if [[ $test_target != "" ]]
then
    ./scripts/format.sh --no-install
    pytest $1
else
    ./scripts/format.sh --no-install
    ./scripts/lint.sh --no-install
    pytest
    ./scripts/run_mypy.sh --no-install
fi
