import base64
import logging
from typing import List

from slack_bolt.app import App
from slack_bolt.logger import get_bolt_app_logger
from slack_bolt.oauth.oauth_flow import OAuthFlow
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
        self.logger.debug(f"Incoming event: {event}, context: {context}")

        method = event.get("requestContext", {}).get("http", {}).get("method", None)
        if method is None:
            return not_found()
        if method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: OAuthFlow = self.app.oauth_flow
                bolt_req = to_bolt_request(event)
                query = bolt_req.query
                is_callback = (query.get("code", None) is not None \
                               and query.get("state", None) is not None) \
                              or query.get("error", None) is not None
                if is_callback:
                    bolt_resp = oauth_flow.handle_callback(bolt_req)
                    return to_aws_response(bolt_resp)
                else:
                    bolt_resp = oauth_flow.handle_installation(bolt_req)
                    return to_aws_response(bolt_resp)
        elif method == "POST":
            bolt_req = to_bolt_request(event)
            bolt_resp = self.app.dispatch(bolt_req)
            aws_response = to_aws_response(bolt_resp)
            return aws_response

        return not_found()


def to_bolt_request(event):
    body = event.get("body", "")
    if event["isBase64Encoded"]:
        body = base64.b64decode(body).decode("utf-8")
    cookies: List[str] = event.get("cookies", [])
    headers = event.get("headers", {})
    headers["cookie"] = cookies
    return BoltRequest(
        body=body,
        query=event.get("queryStringParameters", {}),
        headers=headers,
    )


def to_aws_response(resp: BoltResponse):
    return {
        "statusCode": resp.status,
        "body": resp.body,
        "headers": resp.first_headers(),
    }


def not_found():
    return {
        "statusCode": 404,
        "body": "Not Found",
        "headers": {},
    }
