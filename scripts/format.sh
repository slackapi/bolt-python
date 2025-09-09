#!/bin/bash
# ./scripts/format.sh

script_dir=`dirname $0`
cd ${script_dir}/..

pip install -U pip
pip install -U -r requirements/tools.txt

black slack_bolt/ tests/
