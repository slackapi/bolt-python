#!/bin/bash
rm -rf vendor && mkdir -p vendor/slack_bolt && cp -pr ../../slack_bolt/* vendor/slack_bolt/
pip install git+https://github.com/nficano/python-lambda
lambda deploy \
  --config-file aws_lambda_config.yaml \
  --requirements requirements.txt
