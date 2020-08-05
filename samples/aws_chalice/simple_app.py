import logging
import time

from chalice import Chalice, Response
from slack_bolt import App
from slack_bolt.adapter.aws_lambda.chalice_handler import ChaliceSlackRequestHandler

# process_before_response must be True when running on FaaS
bolt_app = App(process_before_response=True)


@bolt_app.event("app_mention")
def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    say("What's up? I'm a Chalice app :wave:")


ChaliceSlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# Don't change this variable name "app"
app = Chalice(app_name="bolt-python-chalice")
slack_handler = ChaliceSlackRequestHandler(app=bolt_app, chalice=app)


def respond_to_slack_within_3_seconds(ack):
    # This method is for synchronous communication with the Slack API server
    ack("Thanks!")


def can_be_long(say):
    # This can be executed in a thread, asyncio's Future, a new AWS lambda function
    # ack() is not allowed here
    time.sleep(5)
    say("I'm done!")


bolt_app.command("/hello-bolt-python-chalice")(
    ack=respond_to_slack_within_3_seconds, subsequent=[can_be_long],
)


@app.route(
    "/slack/events",
    methods=["POST"],
    content_types=["application/x-www-form-urlencoded", "application/json"],
)
def events() -> Response:
    return slack_handler.handle(app.current_request)


# configure aws credentials properly
# pip install -r requirements.txt
# edit .chalice/config.json
# rm -rf vendor/latest_slack_bolt && cp -pr ../../src vendor/latest_slack_bolt
# chalice deploy

# for local dev
# chalice local --stage dev --port 3000
