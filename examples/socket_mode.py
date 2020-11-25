# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "..")
# ------------------------------------------------

import logging
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode.websocket_client import SocketModeHandler

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.command("/hello-socket-mode")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


@app.event("app_mention")
def event_test(event, say):
    say(f"Hi there, <@{event['user']}>!")


@app.shortcut("socket-mode")
def global_shortcut(ack):
    ack()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # export SLACK_APP_TOKEN=xapp-***
    # export SLACK_BOT_TOKEN=xoxb-***
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
