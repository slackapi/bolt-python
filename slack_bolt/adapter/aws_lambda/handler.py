import base64
import logging
from typing import Dict, Any, Sequence

from slack_bolt.adapter.aws_lambda.internals import _first_value
from slack_bolt.adapter.aws_lambda.lazy_listener_runner import LambdaLazyListenerRunner
from slack_bolt.app import App
from slack_bolt.logger import get_bolt_app_logger
from slack_bolt.oauth import OAuthFlow
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class SlackRequestHandler:
    def __init__(self, app: App):
        self.app = app
        self.logger = get_bolt_app_logger(app.name, SlackRequestHandler, app.logger)
        self.app.listener_runner.lazy_listener_runner = LambdaLazyListenerRunner(self.logger)
        if self.app.oauth_flow is not None:
            self.app.oauth_flow.settings.redirect_uri_page_renderer.install_path = "?"

    @classmethod
    def clear_all_log_handlers(cls):
        # https://stackoverflow.com/questions/37703609/using-python-logging-with-aws-lambda
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)

    def handle(self, event, context):
        self.logger.debug(f"Incoming event: {event}, context: {context}")

        method = event.get("requestContext", {}).get("http", {}).get("method")
        if method is None:
            method = event.get("requestContext", {}).get("httpMethod")

        if method is None:
            return not_found()
        if method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: OAuthFlow = self.app.oauth_flow
                bolt_req: BoltRequest = to_bolt_request(event)
                query = bolt_req.query
                is_callback = query is not None and (
                    (_first_value(query, "code") is not None and _first_value(query, "state") is not None)
                    or _first_value(query, "error") is not None
                )
                if is_callback:
                    bolt_resp = oauth_flow.handle_callback(bolt_req)
                    return to_aws_response(bolt_resp)
                else:
                    bolt_resp = oauth_flow.handle_installation(bolt_req)
                    return to_aws_response(bolt_resp)
        elif method == "POST":
            bolt_req = to_bolt_request(event)
            # https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
            aws_lambda_function_name = context.function_name
            bolt_req.context["aws_lambda_function_name"] = aws_lambda_function_name
            bolt_req.context["aws_lambda_invoked_function_arn"] = context.invoked_function_arn
            bolt_req.context["lambda_request"] = event
            bolt_resp = self.app.dispatch(bolt_req)
            aws_response = to_aws_response(bolt_resp)
            return aws_response
        elif method == "NONE":
            bolt_req = to_bolt_request(event)
            bolt_resp = self.app.dispatch(bolt_req)
            aws_response = to_aws_response(bolt_resp)
            return aws_response

        return not_found()


def to_bolt_request(event) -> BoltRequest:
    # API Gateway sends null (not a missing key) for fields that have no value,
    # such as "headers", "multiValueHeaders" and "queryStringParameters".
    # Every lookup below treats None the same as a missing key.
    body = event.get("body") or ""
    if event.get("isBase64Encoded") is True and body:
        body = base64.b64decode(body).decode("utf-8")
    cookies: Sequence[str] = event.get("cookies") or []
    if len(cookies) == 0:
        # In the case of format v1
        multiValueHeaders = event.get("multiValueHeaders") or {}
        cookies = multiValueHeaders.get("cookie") or []
        if len(cookies) == 0:
            # Try using uppercase
            cookies = multiValueHeaders.get("Cookie") or []
    # Copy the headers so the caller's event dict is left untouched
    headers = dict(event.get("headers") or {})
    headers["cookie"] = cookies
    return BoltRequest(
        body=body,
        query=event.get("queryStringParameters") or {},
        headers=headers,
    )


def to_aws_response(resp: BoltResponse) -> Dict[str, Any]:
    return {
        "statusCode": resp.status,
        "body": resp.body,
        "headers": resp.first_headers(),
    }


def not_found() -> Dict[str, Any]:
    return {
        "statusCode": 404,
        "body": "Not Found",
        "headers": {},
    }
