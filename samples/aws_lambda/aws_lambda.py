# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "vendor")
# ------------------------------------------------

import logging

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)


@app.event("app_mention")
def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    say("What's up?")


@app.command("/hello-bolt-python-lambda")
def respond_to_slack_within_3_seconds(ack):
    ack("Thanks!")


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)

# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***

# rm -rf vendor && cp -pr ../../src/* vendor/
# pip install python-lambda
# lambda deploy --config-file aws_lambda_config.yaml --requirements requirements.txt
