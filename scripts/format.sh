#!/bin/bash
# ./scripts/format.sh

script_dir=`dirname $0`
cd ${script_dir}/..

if [[ "$1" != "--no-install" ]]; then
    export PIP_REQUIRE_VIRTUALENV=1
    pip install -U pip
    pip install -U -r requirements/dev_tools.txt
fi

black slack_bolt/ tests/
