#!/bin/bash
# Generate API documents from the latest source code

script_dir=`dirname $0`
cd ${script_dir}/..

pip install -U pdoc3
rm -rf docs/reference

pdoc slack_bolt --html -o docs/reference
cp -R docs/reference/slack_bolt/* docs/reference/
rm -rf docs/reference/slack_bolt

open docs/reference/index.html
