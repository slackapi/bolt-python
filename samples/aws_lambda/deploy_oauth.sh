#!/bin/bash
rm -rf vendor && cp -pr ../../src vendor
pip install python-lambda -U
lambda deploy \
  --config-file aws_lambda_oauth_config.yaml \
  --requirements requirements_oauth.txt