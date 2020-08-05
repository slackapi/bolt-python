# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "..")
# ------------------------------------------------

import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
from slack_bolt.oauth import OAuthFlow

app = App(oauth_flow=OAuthFlow.sqlite3(database="./slackapp.db"))


@app.event("app_mention")
def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    say("What's up?")


if __name__ == "__main__":
    app.start(3000)

# pip install -i https://test.pypi.org/simple/ slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,channels:history,im:history,chat:write
# python oauth_app.py
