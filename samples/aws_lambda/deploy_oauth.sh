#!/bin/bash
rm -rf ./src
cp -pr ../../src src
pip install python-lambda -U
lambda deploy \
  --config-file aws_lambda_oauth_config.yaml \
  --requirements requirements_oauth.txt