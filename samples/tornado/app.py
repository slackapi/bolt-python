# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../..")
# ------------------------------------------------

import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
from slack_bolt.adapter.tornado import SlackEventsHandler

app = App()


@app.middleware  # or app.use(log_request)
def log_request(logger, payload, next):
    logger.debug(payload)
    return next()


@app.event("app_mention")
def event_test(ack, payload, say, logger):
    logger.info(payload)
    say("What's up?")


from tornado.web import Application
from tornado.ioloop import IOLoop

api = Application([("/slack/events", SlackEventsHandler, dict(app=app))])

if __name__ == "__main__":
    api.listen(3000)
    IOLoop.current().start()

# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python app.py
