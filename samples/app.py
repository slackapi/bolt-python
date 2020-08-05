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


@app.event("app_mention")
def event_test(payload, say, logger):
    logger.info(payload)
    say("What's up?")


if __name__ == "__main__":
    app.start(3000)

# pip install -i https://test.pypi.org/simple/ slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python app.py
