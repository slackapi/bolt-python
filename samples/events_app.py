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


if __name__ == "__main__":
    app.start(3000)

# pip install slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python events_app.py
