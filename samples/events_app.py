# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "..")
# ------------------------------------------------

import re
import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App

app = App()


@app.middleware  # or app.use(log_request)
def log_request(logger, payload, next):
    logger.debug(payload)
    return next()


@app.event("app_mention")
def event_test(payload, say, logger):
    logger.info(payload)
    say("What's up?")


@app.message("test")
def test_message(logger, payload):
    logger.info(payload)


@app.message(re.compile("bug"))
def mention_bug(logger, payload):
    logger.info(payload)


@app.event(
    event={"type": "message", "subtype": "message_deleted"},
    matchers=[
        lambda payload: payload["event"]["previous_message"].get("bot_id", None) is None
    ],
)
def deleted(payload, say):
    message = payload["event"]["previous_message"]["text"]
    say(f"I've noticed you deleted: {message}")


def print_bot(req, resp, next):
    bot_id = req.global_shortcut_payload["event"]["previous_message"]["bot_id"]
    logger = logging.getLogger(__name__)
    logger.info(f"bot_id surely exists here: {bot_id}")
    return next()


@app.event(
    event={"type": "message", "subtype": "message_deleted"},
    matchers=[lambda payload: payload["event"]["previous_message"].get("bot_id", None)],
    middleware=[print_bot],
)
def bot_message_deleted(logger):
    logger.info("A bot message has been deleted")


if __name__ == "__main__":
    app.start(3000)

# pip install slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python events_app.py
