#!/bin/bash

./scripts/run_tests.sh && \
  pip install -U pip && \
  pip install twine wheel && \
  rm -rf dist/ build/ slack_bolt.egg-info/ && \
  python setup.py sdist bdist_wheel && \
  twine check dist/*