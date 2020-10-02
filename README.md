# Bolt for Python

[![Python Version][python-version]][pypi-url]
[![pypi package][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]
[![Codecov][codecov-image]][codecov-url]

A Python framework to build Slack apps in a flash with the latest platform features. Check the [document](https://slack.dev/bolt-python/) and [examples](https://github.com/slackapi/bolt-python/tree/main/examples) to know how to use this framework.

## Setup

```bash
# Python 3.6+ required
python -m venv .venv
source .venv/bin/activate

pip install -U pip
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

# Events API: https://api.slack.com/events-api
@app.event("app_mention")
def event_test(say):
    say("What's up?")

# Interactivity: https://api.slack.com/interactivity
@app.shortcut("callback-id-here")
# @app.command("/hello-bolt-python")
def open_modal(ack, client, logger, body):
    # acknowledge the incoming request from Slack immediately
    ack()
    # open a modal
    api_response = client.views_open(
        trigger_id=body["trigger_id"],
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
def view_submission(ack, view, logger):
    ack()
    # Prints {'b': {'a': {'type': 'plain_text_input', 'value': 'Your Input'}}}
    logger.info(view["state"]["values"])

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

## AsyncApp Setup

If you prefer building Slack apps using [asyncio](https://docs.python.org/3/library/asyncio.html), you can go with `AsyncApp` instead. You can use async/await style for everything in the app. To use `AsyncApp`, [AIOHTTP](https://docs.aiohttp.org/en/stable/) library is required for asynchronous Slack Web API calls and the default web server.

```bash
# Python 3.6+ required
python -m venv .venv
source .venv/bin/activate

pip install -U pip
# aiohttp is required
pip install slack_bolt aiohttp
```

Import `slack_bolt.async_app.AsyncApp` instead of `slack_bolt.App`. All middleware/listeners must be async functions. Inside the functions, all utility methods such as `ack`, `say`, and `respond` requires `await` keyword.

```python
from slack_bolt.async_app import AsyncApp

app = AsyncApp()

@app.event("app_mention")
async def event_test(body, say, logger):
    logger.info(body)
    await say("What's up?")

@app.command("/hello-bolt-python")
async def command(ack, body, respond):
    await ack()
    await respond(f"Hi <@{body['user_id']}>!")

if __name__ == "__main__":
    app.start(3000)
```

Starting the app is exactly the same with the way using `slack_bolt.App`.

```bash
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
python app.py

# in another terminal
ngrok http 3000
```

If you want to use another async Web framework (e.g., Sanic, FastAPI, Starlette), take a look at the built-in adapters and their examples.

* [The Bolt app examples](https://github.com/slackapi/bolt-python/tree/main/examples)
* [The built-in adapters](https://github.com/slackapi/bolt-python/tree/main/slack_bolt/adapter)

# Feedback

We are keen to hear your feedback. Please feel free to [submit an issue](https://github.com/slackapi/bolt-python/issues)!

# License

The MIT License

[pypi-image]: https://badge.fury.io/py/slack-bolt.svg
[pypi-url]: https://pypi.org/project/slack-bolt/
[travis-image]: https://travis-ci.org/slackapi/bolt-python.svg?branch=main
[travis-url]: https://travis-ci.org/slackapi/bolt-python
[codecov-image]: https://codecov.io/gh/slackapi/bolt-python/branch/main/graph/badge.svg
[codecov-url]: https://codecov.io/gh/slackapi/bolt-python
[python-version]: https://img.shields.io/pypi/pyversions/slack-bolt.svg
