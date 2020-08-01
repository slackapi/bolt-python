#!/bin/bash

# configure aws credentials properly
pip install -r requirements.txt
# edit .chalice/config.json
rm -rf vendor/latest_slack_bolt && cp -pr ../../src vendor/latest_slack_bolt
chalice deploy
