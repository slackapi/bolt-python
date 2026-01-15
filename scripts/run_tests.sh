#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/run_tests.sh
# single: ./scripts/run_tests.sh tests/scenario_tests/test_app.py

script_dir=`dirname $0`
cd ${script_dir}/..

test_target="$1"

./scripts/format.sh --no-install

if [[ $test_target != "" ]]
then
  pytest -vv $1
else
  pytest
fi
