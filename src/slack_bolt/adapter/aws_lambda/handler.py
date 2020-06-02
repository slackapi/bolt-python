import base64
import logging

from slack_bolt.app import App
from slack_bolt.logger import get_bolt_app_logger
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse

# https://stackoverflow.com/questions/37703609/using-python-logging-with-aws-lambda
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)


class SlackRequestHandler():
    def __init__(self, app: App):
        self.app = app
        self.logger = get_bolt_app_logger(app.name, SlackRequestHandler)

    def handle(self, event, context):
        bolt_req = to_bolt_request(event)
        bolt_resp = self.app.dispatch(bolt_req)
        aws_response = to_aws_response(bolt_resp)
        return aws_response


def to_bolt_request(event):
    body = event["body"]
    if event["isBase64Encoded"]:
        body = base64.b64decode(body).decode("utf-8")
    return BoltRequest(
        body=body,
        headers=event["headers"],
    )


def to_aws_response(resp: BoltResponse):
    return {
        "statusCode": resp.status,
        "body": resp.body,
        "headers": resp.headers,
    }
