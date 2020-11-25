# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys


sys.path.insert(1, "..")
# ------------------------------------------------

import logging
import os

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler

# Install the Slack app and get xoxb- token in advance
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])


@app.command("/hello-socket-mode")
async def hello_command(ack, body):
    user_id = body["user_id"]
    await ack(f"Hi <@{user_id}>!")


@app.event("app_mention")
async def event_test(event, say):
    await say(f"Hi there, <@{event['user']}>!")


@app.shortcut("socket-mode")
async def global_shortcut(ack):
    await ack()


# export SLACK_APP_TOKEN=xapp-***
# export SLACK_BOT_TOKEN=xoxb-***

async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    import asyncio
    asyncio.run(main())
