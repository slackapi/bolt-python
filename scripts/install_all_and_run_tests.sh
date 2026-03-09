#!/bin/bash
# Run all the tests or a single test
# all: ./scripts/install_all_and_run_tests.sh
# single: ./scripts/install_all_and_run_tests.sh tests/scenario_tests/test_app.py

script_dir=`dirname $0`
cd ${script_dir}/..

test_target="${1:-tests/}"

# keep in sync with LATEST_SUPPORTED_PY in .github/workflows/ci-build.yml
LATEST_SUPPORTED_PY="3.14"
current_py=$(python --version | sed -E 's/Python ([0-9]+\.[0-9]+).*/\1/')

./scripts/install.sh

./scripts/format.sh --no-install
./scripts/lint.sh --no-install
pytest $test_target

if [[ "$current_py" == "$LATEST_SUPPORTED_PY" ]]; then
    ./scripts/run_mypy.sh --no-install
fi
