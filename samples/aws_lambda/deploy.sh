#!/bin/bash
rm -rf vendor && cp -pr ../../src vendor
pip install python-lambda -U
lambda deploy \
  --config-file aws_lambda_config.yaml \
  --requirements requirements.txt