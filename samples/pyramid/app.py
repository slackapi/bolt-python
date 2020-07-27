# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../../src")
# ------------------------------------------------


import logging
import re
from slack_bolt import App, Respond, Ack
from slack_bolt.adapter.pyramid.handler import SlackRequestHandler
from slack_sdk import WebClient

logging.basicConfig(level=logging.DEBUG)
app = App()


# @app.command("/bolt-py-proto", [lambda payload: payload["team_id"] == "T03E94MJU"])
def test_command(logger: logging.Logger, payload: dict, ack: Ack, respond: Respond):
    logger.info(payload)
    respond(blocks=[
        {
            "type": "section",
            "block_id": "b",
            "text": {
                "type": "mrkdwn",
                "text": "You can add a button alongside text in your message. "
            },
            "accessory": {
                "type": "button",
                "action_id": "a",
                "text": {
                    "type": "plain_text",
                    "text": "Button"
                },
                "value": "click_me_123"
            }
        }
    ])
    return ack("thanks!")


app.command(re.compile(r"/bolt-.+"))(test_command)


@app.shortcut("test-shortcut")
def test_shortcut(ack, client: WebClient, logger, payload):
    logger.info(payload)
    ack()
    res = client.views_open(
        trigger_id=payload["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "view-id",
            "title": {
                "type": "plain_text",
                "text": "My App",
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Label",
                    }
                }
            ]
        })
    logger.info(res)


@app.view("view-id")
def view_submission(ack, payload, logger):
    logger.info(payload)
    ack()


@app.action("a")
def button_click(logger, payload, say, ack, respond):
    logger.info(payload)
    ack()
    respond("respond!")
    # say(text="say!")


@app.event("app_mention")
def event_test(ack, payload, say, logger):
    logger.info(payload)
    say("What's up?")


handler = SlackRequestHandler(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator

    with Configurator() as config:
        config.add_route('slack_events', '/slack/events')
        config.add_view(handler.handle, route_name='slack_events', request_method='POST')

        config.add_route('slack_install', '/slack/install')
        config.add_route('slack_oauth_redirect', '/slack/oauth_redirect')
        config.add_view(handler.handle, route_name='slack_install', request_method='GET')
        config.add_view(handler.handle, route_name='slack_oauth_redirect', request_method='GET')

        pyramid_app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 3000, pyramid_app)
    server.serve_forever()

# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***

# # -- OAuth flow -- #
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,channels:history,im:history,chat:write

# python app.py