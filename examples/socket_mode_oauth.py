# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "..")
# ------------------------------------------------

import logging
import os
from slack_bolt.app import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.adapter.socket_mode.websocket_client import SocketModeHandler

app = App(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    oauth_settings=OAuthSettings(
        client_id=os.environ["SLACK_CLIENT_ID"],
        client_secret=os.environ["SLACK_CLIENT_SECRET"],
        scopes=os.environ["SLACK_SCOPES"].split(","),
    )
)


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
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).connect()
    app.start()

    # export SLACK_APP_TOKEN=
    # export SLACK_SIGNING_SECRET=
    # export SLACK_CLIENT_ID=
    # export SLACK_CLIENT_SECRET=
    # export SLACK_SCOPES=
    # pip install .[optional]
    # pip install slack_bolt
    # python socket_mode_oauth.py
