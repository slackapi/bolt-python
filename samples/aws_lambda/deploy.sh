#!/bin/bash
rm -rf ./src
cp -pr ../../src src
pip install python-lambda -U
lambda deploy \
  --config-file aws_lambda_config.yaml \
  --requirements requirements.txt