#!/bin/bash

pip install -U pip && \
  python setup.py test && \
  pip install twine wheel && \
  rm -rf dist/ build/ slack_bolt.egg-info/ && \
  python setup.py sdist bdist_wheel && \
  twine check dist/* && \
  twine upload --repository testpypi dist/*
