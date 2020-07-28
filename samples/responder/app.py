# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../../src")
# ------------------------------------------------

from slack_bolt import App
from slack_bolt.adapter.responder import SlackRequestHandler

app = App()
app_handler = SlackRequestHandler(app)


@app.event("app_mention")
def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    say("What's up?")


from responder import API, Request, Response

api = API()


@api.route("/slack/events")
async def endpoint(req: Request, resp: Response):
    return await app_handler.handle(req, resp)

# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# uvicorn app:api --reload --port 3000 --log-level debug
