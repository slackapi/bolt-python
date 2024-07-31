#!/bin/bash
# Generate API documents from the latest source code

script_dir=`dirname $0`
cd ${script_dir}/..

pip install -U pdoc3
rm -rf docs/static/api-docs
pdoc slack_bolt --html -o docs/static/api-docs
open docs/static/api-docs/slack_bolt/index.html
