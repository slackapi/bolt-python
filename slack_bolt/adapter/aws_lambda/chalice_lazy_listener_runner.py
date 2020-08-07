import json
from logging import Logger
from typing import Callable

import boto3

from slack_bolt import BoltRequest
from slack_bolt.lazy_listener import LazyListenerRunner


class ChaliceLazyListenerRunner(LazyListenerRunner):
    def __init__(self, logger: Logger):
        self.lambda_client = boto3.client("lambda")
        self.logger = logger

    def start(self, function: Callable[..., None], request: BoltRequest) -> None:
        chalice_request: dict = request.context["chalice_request"]
        request.headers["x-slack-bolt-lazy-only"] = ["1"]
        request.headers["x-slack-bolt-lazy-function-name"] = [
            request.lazy_function_name
        ]
        payload = {
            "method": "NONE",
            "headers": {k: v[0] for k, v in request.headers.items()},
            "multiValueQueryStringParameters": request.query,
            "queryStringParameters": {k: v[0] for k, v in request.query.items()},
            "pathParameters": {},
            "stageVariables": {},
            "requestContext": chalice_request["context"],
            "body": request.body,
            "isBase64Encoded": False,
        }
        invocation = self.lambda_client.invoke(
            FunctionName=request.context["aws_lambda_function_name"],
            InvocationType="Event",
            Payload=json.dumps(payload),
        )
        self.logger.info(invocation)
