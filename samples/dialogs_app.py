# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "..")
# ------------------------------------------------

import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App

app = App()


@app.middleware  # or app.use(log_request)
def log_request(logger, payload, next):
    logger.debug(payload)
    return next()


@app.command("/hello-bolt-python")
def test_command(payload, client, ack, logger):
    logger.info(payload)
    ack("I got it!")
    res = client.dialog_open(
        trigger_id=payload["trigger_id"],
        dialog={
            "callback_id": "dialog-callback-id",
            "title": "Request a Ride",
            "submit_label": "Request",
            "notify_on_cancel": True,
            "state": "Limo",
            "elements": [
                {"type": "text", "label": "Pickup Location", "name": "loc_origin"},
                {
                    "type": "text",
                    "label": "Dropoff Location",
                    "name": "loc_destination",
                },
                {
                    "label": "Type",
                    "name": "types",
                    "type": "select",
                    "data_source": "external",
                },
            ],
        },
    )
    logger.info(res)


@app.action({"type": "dialog_submission", "callback_id": "dialog-callback-id"})
def dialog_submission(ack):
    ack()


@app.options({"type": "dialog_suggestion", "callback_id": "dialog-callback-id"})
def dialog_suggestion(ack):
    ack(
        {
            "options": [
                {
                    "label": "[UXD-342] The button color should be artichoke green, not jalapeño",
                    "value": "UXD-342",
                },
                {"label": "[FE-459] Remove the marquee tag", "value": "FE-459"},
                {
                    "label": "[FE-238] Too many shades of gray in master CSS",
                    "value": "FE-238",
                },
            ]
        }
    )


@app.action({"type": "dialog_cancellation", "callback_id": "dialog-callback-id"})
def dialog_cancellation(ack):
    ack()


if __name__ == "__main__":
    app.start(3000)

# pip install -i https://test.pypi.org/simple/ slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python dialogs_app.py
