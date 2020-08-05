# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "..")
# ------------------------------------------------

import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt.async_app import AsyncApp

app = AsyncApp()


@app.middleware  # or app.use(log_request)
async def log_request(logger, payload, next):
    logger.debug(payload)
    return await next()


@app.event("app_mention")
async def event_test(payload, say, logger):
    logger.info(payload)
    await say("What's up?")


@app.command("/hello-bolt-python")
# or app.command(re.compile(r"/hello-.+"))(test_command)
async def command(ack):
    await ack("Thanks!")


if __name__ == "__main__":
    app.start(3000)

# pip install -i https://test.pypi.org/simple/ slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python app.py
