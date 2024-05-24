from slack_bolt import App
from slack_bolt.adapter.wsgi import SlackRequestHandler

app = App()


@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("What's up?")


api = SlackRequestHandler(app)

# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# gunicorn app:api -b 0.0.0.0:3000 --log-level debug
# ngrok http 3000
