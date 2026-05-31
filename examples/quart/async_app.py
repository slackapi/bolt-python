import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.quart import AsyncSlackRequestHandler

app = AsyncApp()
app_handler = AsyncSlackRequestHandler(app)


@app.event("app_mention")
async def handle_app_mentions(body, say, logger):
    logger.info(body)
    await say("What's up?")


from quart import Quart, request

api = Quart(__name__)


@api.post("/slack/events")
async def endpoint():
    return await app_handler.handle(request)


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))


# Requires Python 3.9+
# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# hypercorn async_app:api --reload --bind 0.0.0.0:3000
