# Bolt for Python

A Python framework to build Slack apps in a flash with the latest platform features.

## Setup

```bash
python -m venv env
source env/bin/activate
pip install -U pip
pip install -U slackclient
pip install -U -i https://test.pypi.org/simple/ slack_bolt
```

## First Bolt App

Create an app by calling a constructor, which is a top-level export.

```python
# app.py
import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack_bolt import App

app = App(
    signing_secret = os.environ["SLACK_SIGNING_SECRET"],
    token= os.environ["SLACK_BOT_TOKEN"],
)

@app.shortcut("callback-id-here")
def handle_global_shortcut(ack, client, logger, payload):
    ack()
    logger.info(payload)
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


@app.view("view-id")
def view_submission(ack, payload, logger):
    ack()
    logger.info(payload)


@app.event("app_mention")
def event_test(ack, say):
    ack()
    say("What's up?")


if __name__ == '__main__':
    app.start(3000) # POST http://localhost:3000/slack/events
```

## Run the Bolt App

```bash
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
python app.py

ngrok http 3000
```
