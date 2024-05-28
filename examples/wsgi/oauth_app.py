from slack_bolt import App
from slack_bolt.adapter.wsgi import SlackRequestHandler

app = App()


@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("What's up?")


api = SlackRequestHandler(app)

# pip install -r requirements.txt

# # -- OAuth flow -- #
# export SLACK_SIGNING_SECRET=***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,channels:history,im:history,chat:write

# gunicorn oauth_app:api -b 0.0.0.0:3000 --log-level debug
