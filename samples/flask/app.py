# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../..")
# ------------------------------------------------

import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

app = App()


@app.middleware  # or app.use(log_request)
def log_request(logger, payload, next):
    logger.debug(payload)
    return next()


@app.event("app_mention")
def event_test(ack, payload, say, logger):
    logger.info(payload)
    say("What's up?")


from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# FLASK_APP=app.py FLASK_ENV=development flask run -p 3000
