# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../../src")
# ------------------------------------------------

from slack_bolt import AsyncApp
from slack_bolt.adapter.starlette import AsyncSlackRequestHandler

app = AsyncApp()


@app.event("app_mention")
async def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    await say("What's up?")


app_handler = AsyncSlackRequestHandler(app)

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route


async def endpoint(req: Request):
    return await app_handler.handle(req)


api = Starlette(
    debug=True,
    routes=[
        Route("/slack/events", endpoint=endpoint, methods=["POST"])
    ]
)

# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# uvicorn async_app:api --reload --port 3000 --log-level debug
