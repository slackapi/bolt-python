# Important Notice

This project is **still in alpha**, and may have bugs in it. Also, the public APIs can be changed until the v1 release.

# Bolt for Python (still in alpha)

A Python framework to build Slack apps in a flash with the latest platform features.

## Setup

```bash
python -m venv env
source env/bin/activate
pip install slack_bolt
```

## First Bolt App (app.py)

Create an app by calling a constructor, which is a top-level export.

```python
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
```

## Run the Bolt App

```bash
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
python app.py

# another terminal
ngrok http 3000
```

# License

The MIT License