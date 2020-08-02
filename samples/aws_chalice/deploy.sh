#!/bin/bash

# configure aws credentials properly
pip install -U chalice click boto3
pip install -r requirements.txt
# edit .chalice/config.json
rm -rf vendor/slack_* && cp -pr ../../src vendor
chalice deploy
