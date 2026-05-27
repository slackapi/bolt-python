#!/bin/bash
# Installs all dependencies of the project
# ./scripts/install.sh

script_dir=`dirname $0`
cd ${script_dir}/..
rm -rf ./slack_bolt.egg-info

# Update pip to prevent warnings
pip install -U pip

# The package causes a conflict with moto
pip uninstall python-lambda

pip install -U -e .
pip install -U -r requirements/test_async.txt
pip install -U -r requirements/adapter_dev.txt
pip install -U -r requirements/test_adapter.txt
pip install -U -r requirements/dev_tools.txt

# To avoid errors due to the old versions of click forced by Chalice
pip install -U pip click
