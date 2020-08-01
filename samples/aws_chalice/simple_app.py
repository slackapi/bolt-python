# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "latest_slack_bolt")
# ------------------------------------------------

import logging
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
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# Don't change this variable name "app"
app = Chalice(app_name="bolt-python-chalice")
slack_handler = ChaliceSlackRequestHandler(app=bolt_app)


@app.route("/slack/events", methods=["POST"])
def events() -> Response:
    return slack_handler.handle(app.current_request)

# configure aws credentials properly
# pip install -r requirements.txt
# edit .chalice/config.json
# rm -rf vendor/latest_slack_bolt && cp -pr ../../src vendor/latest_slack_bolt
# chalice deploy

# for local dev
# chalice local --stage dev --port 3000
