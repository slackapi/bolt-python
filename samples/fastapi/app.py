# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../../src")
# ------------------------------------------------

import logging
import re
from slack_bolt import App, Respond, Ack
from slack_sdk import WebClient
from slack_bolt.adapter.fastapi import SlackRequestHandler

logging.basicConfig(level=logging.DEBUG)
app = App()
app_handler = SlackRequestHandler(app)


# @app.command("/bolt-py-proto", [lambda payload: payload["team_id"] == "T03E94MJU"])
def test_command(logger: logging.Logger, payload: dict, ack: Ack, respond: Respond):
    logger.info(payload)
    respond(blocks=[
        {
            "type": "section",
            "block_id": "b",
            "text": {
                "type": "mrkdwn",
                "text": "You can add a button alongside text in your message. "
            },
            "accessory": {
                "type": "button",
                "action_id": "a",
                "text": {
                    "type": "plain_text",
                    "text": "Button"
                },
                "value": "click_me_123"
            }
        }
    ])
    return ack("thanks!")


app.command(re.compile(r"/bolt-.+"))(test_command)


@app.shortcut("test-shortcut")
def test_shortcut(ack, client: WebClient, logger, payload):
    logger.info(payload)
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
    return ack()


@app.view("view-id")
def view_submission(ack, payload, logger):
    logger.info(payload)
    return ack()


@app.action("a")
def button_click(logger, payload, say, ack, respond):
    logger.info(payload)
    respond("respond!")
    # say(text="say!")
    return ack()


from fastapi import FastAPI, Request

api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)

# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# uvicorn app:api --reload --port 3000
