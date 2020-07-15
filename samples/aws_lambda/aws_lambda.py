# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "src")
# ------------------------------------------------

import logging
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler, LambdaS3OAuthFlow

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

app = App(
    process_before_response=True,
    oauth_flow=LambdaS3OAuthFlow(),
)


@app.shortcut("bolt-python-on-aws-lambda")
def command_handler(logger, payload, client, ack):
    res = client.views_open(
        trigger_id=payload["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "view-id",
            "title": {
                "type": "plain_text",
                "text": "My App",
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Label",
                    }
                }
            ]
        })
    logger.info(res)
    return ack("Thanks!")


@app.view("view-id")
def view_submission(ack, payload, logger):
    logger.info(payload)
    return ack()


@app.event("app_mention")
def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    say("What's up?")

slack_handler = SlackRequestHandler(app=app)


def handler(event, context):
    return slack_handler.handle(event, context)

# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***

# rm -rf src
# cp -pr ../../src src
# pip install python-lambda
# lambda deploy --config-file aws_lambda_config.yaml --requirements requirements.txt

# # -- OAuth flow -- #
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,channels:history,im:history,chat:write

# AWS IAM Role: bolt_python_s3_storage
#   - AmazonS3FullAccess
#   - AWSLambdaBasicExecutionRole

# rm -rf src
# cp -pr ../../src src
# pip install python-lambda
# lambda deploy --config-file aws_lambda_config.yaml --requirements requirements.txt
