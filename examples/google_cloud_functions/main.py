# https://cloud.google.com/functions/docs/first-python

import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)


@app.command("/hello-bolt-python-gcp")
def hello_command(ack):
    ack("Hi from Google Cloud Functions!")


@app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)
    say("Hi from Google Cloud Functions!")


# Flask adapter
from slack_bolt.adapter.flask import SlackRequestHandler

handler = SlackRequestHandler(app)

# Cloud Function
def hello_bolt_app(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    return handler.handle(request)


# Step1: Create a new Slack App: https://api.slack.com/apps
# Bot Token Scopes: chat:write, commands, app_mentions:read

# Step2: Set env variables
# cp .env.yaml.sample .env.yaml
# vi .env.yaml

# Step3: Create a new Google Cloud project
# gcloud projects create YOUR_PROJECT_NAME
# gcloud config set project YOUR_PROJECT_NAME

# Step4: Deploy a function in the project
# gcloud functions deploy hello_bolt_app --runtime python38 --trigger-http --allow-unauthenticated --env-vars-file .env.yaml
# gcloud functions describe hello_bolt_app

# Step5: Set Request URL
# Set https://us-central1-YOUR_PROJECT_NAME.cloudfunctions.net/hello_bolt_app to the following:
#  * slash command: /hello-bolt-python-gcp
#  * Events Subscriptions & add `app_mention` event
