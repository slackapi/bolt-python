#!/bin/bash
rm -rf latest_slack_bolt && cp -pr ../../src latest_slack_bolt
pip install python-lambda -U
lambda deploy \
  --config-file aws_lambda_config.yaml \
  --requirements requirements.txt