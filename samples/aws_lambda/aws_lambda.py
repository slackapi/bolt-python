# ------------------------------------------------
# instead of slack_bolt==0.1.0 in requirements.txt
import sys

sys.path.insert(1, "src")
# ------------------------------------------------

import logging
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
app = App(process_before_response=True)


@app.command("/bolt-py-proto")
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


def handler(event, context):
    return SlackRequestHandler(app).handle(event, context)

# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# cp -pr ../../src src
# pip install python-lambda
# lambda deploy --config-file aws_lambda_config.yaml --requirements requirements.txt
