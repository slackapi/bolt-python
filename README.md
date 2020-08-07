# ⚠️ Important Notice ⚠️

## 🔄 Still Work In Progress 🔄

This project is **still in alpha**, and may have bugs in it. Also, the public APIs can be changed until the v1 release. We are keen to hear your feedback. Please feel free to [submit an issue](https://github.com/slackapi/bolt-python/issues)!

# Bolt for Python (still in alpha)

[![Python Version][python-version]][pypi-url]
[![pypi package][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]

A Python framework to build Slack apps in a flash with the latest platform features. Check the [samples](https://github.com/slackapi/bolt-python/tree/main/samples) to know how to use this framework.

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
logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App

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
@app.shortcut("callback-id-here")
# @app.command("/hello-bolt-python")
def open_modal(ack, client, logger, payload):
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

# in another terminal
ngrok http 3000
```

# Feedback

We are keen to hear your feedback. Please feel free to [submit an issue](https://github.com/slackapi/bolt-python/issues)!

# License

The MIT License

[pypi-image]: https://badge.fury.io/py/slack-bolt.svg
[pypi-url]: https://pypi.org/project/slack-bolt/
[travis-image]: https://travis-ci.org/slackapi/bolt-python.svg?branch=main
[travis-url]: https://travis-ci.org/slackapi/bolt-python
[python-version]: https://img.shields.io/pypi/pyversions/slack-bolt.svg
