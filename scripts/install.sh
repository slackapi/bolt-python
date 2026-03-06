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
pip install -U -r requirements/testing.txt
pip install -U -r requirements/adapter.txt
pip install -U -r requirements/adapter_testing.txt
pip install -U -r requirements/tools.txt

# To avoid errors due to the old versions of click forced by Chalice
pip install -U pip click
