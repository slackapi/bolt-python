#!/bin/bash
# Generate the Markdown API reference from the latest source code.
# The heavy lifting (including inlining re-exported classes) lives in
# scripts/generate_api_docs.py.

set -e
script_dir=$(dirname "$0")
cd "${script_dir}/.."

pip install -U pip
pip install -U -r requirements/adapter_dev.txt
pip install -U -r requirements/async_dev.txt
pip install -U pydoc-markdown
pip install .
rm -rf docs/reference

python scripts/generate_api_docs.py
