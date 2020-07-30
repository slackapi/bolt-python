# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "src")
# ------------------------------------------------

import logging
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler, LambdaS3OAuthFlow

# process_before_response must be True when running on FaaS
app = App(
    process_before_response=True,
    oauth_flow=LambdaS3OAuthFlow(),
)


@app.event("app_mention")
def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    say("What's up?")


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)

# # -- OAuth flow -- #
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# export SLACK_CLIENT_ID=111.111
# export SLACK_CLIENT_SECRET=***
# export SLACK_SCOPES=app_mentions:read,chat:write

# AWS IAM Role: bolt_python_s3_storage
#   - AmazonS3FullAccess
#   - AWSLambdaBasicExecutionRole

# rm -rf src
# cp -pr ../../src src
# pip install python-lambda
# lambda deploy --config-file aws_lambda_oauth_config.yaml --requirements requirements_oauth.txt
