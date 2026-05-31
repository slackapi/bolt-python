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


@api.get("/slack/install")
async def install():
    return await app_handler.handle(request)


@api.get("/slack/oauth_redirect")
async def oauth_redirect():
    return await app_handler.handle(request)


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))


# pip install -r requirements.txt

# # -- OAuth flow -- #
# export SLACK_SIGNING_SECRET=***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,channels:history,im:history,chat:write

# hypercorn async_oauth_app:api --reload --bind 0.0.0.0:3000
