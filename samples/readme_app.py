import logging

from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
app = App()


# Middleware
@app.middleware  # or app.use(log_request)
def log_request(logger, payload, next):
    logger.info(payload)
    return next()


# Events API: https://api.slack.com/events-api
@app.event("app_mention")
def event_test(say):
    say("What's up?")


# Interactivity: https://api.slack.com/interactivity
# @app.shortcut("callback-id-here")
@app.command("/hello-bolt-python")
def handle_global_shortcut(ack, client, logger, payload):
    # acknowledge the incoming request from Slack immediately
    ack()
    # open a modal
    api_response = client.views_open(
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
            "blocks": [
                {
                    "type": "input",
                    "block_id": "b",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "a"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Label",
                    }
                }
            ]
        })
    logger.debug(api_response)


@app.view("view-id")
def view_submission(ack, payload, logger):
    ack()
    # Prints {'b': {'a': {'type': 'plain_text_input', 'value': 'Your Input'}}}
    logger.info(payload["view"]["state"]["values"])


if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
