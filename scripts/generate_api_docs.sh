#!/bin/bash
# Generate the Markdown API reference from the latest source code

set -e
script_dir=$(dirname "$0")
cd "${script_dir}/.."

if [[ "$1" != "--no-install" ]]; then
    pip install -U pip
    pip install -U -r requirements/adapter_dev.txt
    pip install -U -r requirements/async_dev.txt
    pip install -U -r requirements/docs.txt
    pip install .
fi

rm -rf docs/english/reference

python scripts/generate_api_docs.py
