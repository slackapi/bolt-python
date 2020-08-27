# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../../src")
# ------------------------------------------------

import logging
from slack_bolt import App
from slack_bolt.adapter.cherrypy import SlackRequestHandler

logging.basicConfig(level=logging.DEBUG)
app = App()


@app.middleware  # or app.use(log_request)
def log_request(logger, payload, next):
    logger.debug(payload)
    return next()


@app.command("/hello-bolt-python")
def hello_command(ack):
    ack("Hi from CherryPy")


@app.event("app_mention")
def event_test(payload, say, logger):
    logger.info(payload)
    say("What's up?")


import cherrypy

handler = SlackRequestHandler(app)


class SlackApp(object):
    @cherrypy.expose
    @cherrypy.tools.slack_in()
    def events(self, **kwargs):
        return handler.handle()

    @cherrypy.expose
    @cherrypy.tools.slack_in()
    def install(self, **kwargs):
        return handler.handle()

    @cherrypy.expose
    @cherrypy.tools.slack_in()
    def oauth_redirect(self, **kwargs):
        return handler.handle()


if __name__ == "__main__":
    cherrypy.config.update({"server.socket_port": 3000})
    cherrypy.quickstart(SlackApp(), "/slack")

# pip install -r requirements.txt

# # -- OAuth flow -- #
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,chat:write

# python oauth_app.py
