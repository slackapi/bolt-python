#!/bin/bash
# Generate API documents from the latest source code

set -e
script_dir=$(dirname "$0")
cd "${script_dir}/.."

pip install -U pip
pip install -U -r requirements/adapter.txt
pip install -U -r requirements/async.txt
pip install -U pdoc3
pip install .
rm -rf docs/reference

pdoc slack_bolt --html -o docs/reference
cp -R docs/reference/slack_bolt/* docs/reference/
rm -rf docs/reference/slack_bolt

open docs/reference/index.html
