# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import os
import sys

sys.path.insert(1, "../src")
# ------------------------------------------------

import logging
from slack_bolt import App
from slack_sdk.oauth.installation_store.sqlite3 import SQLite3InstallationStore
from slack_sdk.oauth.state_store.sqlite3 import SQLite3OAuthStateStore

logging.basicConfig(level=logging.DEBUG)
app = App(
    installation_store=SQLite3InstallationStore(
        database="./slackapp.db",
        client_id=os.environ["SLACK_CLIENT_ID"],
    ),
    oauth_state_store=SQLite3OAuthStateStore(
        database="./slackapp.db",
        expiration_seconds=120,
    ),
)


def log_request(logger, payload, next):
    logger.debug(payload)
    return next()


app.use(log_request)


@app.event("app_mention")
def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    say("What's up?")


@app.event("message")
def handle_messages():
    pass


if __name__ == '__main__':
    app.start(3000)

# pip install slackclient
# pip install -i https://test.pypi.org/simple/ slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,channels:history,im:history,chat:write
# python oauth_app.py
