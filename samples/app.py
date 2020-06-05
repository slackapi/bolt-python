# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../src")
# ------------------------------------------------

import logging
from slack_bolt import App
from slack_bolt.kwargs_injection import Args
from slack_sdk import WebClient

logging.basicConfig(level=logging.DEBUG)
app = App(process_before_response=True)


@app.middleware  # or app.use(log_request)
def log_request(logger, payload, next):
    logger.debug(payload)
    return next()


@app.command("/bolt-py-proto-2")  # or app.command(re.compile(r"/bolt-.+"))(test_command)
def test_command(args: Args):
    args.logger.info(args.payload)
    respond, ack = args.respond, args.ack

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
    ack("thanks!")


@app.shortcut("test-shortcut")
def test_shortcut(ack, client: WebClient, logger, payload):
    logger.info(payload)
    ack()
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


@app.view("view-id")
def view_submission(ack, payload, logger):
    logger.info(payload)
    return ack()


@app.action("a")
def button_click(logger, payload, ack, respond):
    logger.info(payload)
    respond("respond!")
    # say(text="say!")
    ack()


@app.event("app_mention")
def event_test(ack, payload, say, logger):
    logger.info(payload)
    say("What's up?")
    return ack()


@app.event({"type": "message", "subtype": "message_deleted"})
def deleted(ack, payload, say):
    message = payload["event"]["previous_message"]["text"]
    say(f"I've noticed you deleted: {message}")
    return ack()


@app.event({"type": "message"})
def new_message(ack, logger, payload, say):
    logger.info(payload)
    # say(f"I've noticed you deleted {payload}")
    return ack()


if __name__ == '__main__':
    app.start(3000)

# pip install slackclient
# pip install -i https://test.pypi.org/simple/ slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python app.py
