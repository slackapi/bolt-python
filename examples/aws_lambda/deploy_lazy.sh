#!/bin/bash
rm -rf slack_bolt && mkdir slack_bolt && cp -pr ../../slack_bolt/* slack_bolt/
pip install git+https://github.com/nficano/python-lambda
lambda deploy \
  --config-file lazy_aws_lambda_config.yaml \
  --requirements requirements.txt
