import os
import asyncio

from slack_bolt.middleware.request_parsing import RequestParsing
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


def remove_os_env_temporarily() -> dict:
    old_env = os.environ.copy()
    os.environ.clear()
    for key, value in old_env.items():
        if key.startswith("BOLT_PYTHON_"):
            os.environ[key] = value
    return old_env


def restore_os_env(old_env: dict) -> None:
    os.environ.update(old_env)


def parse_request(req: BoltRequest) -> BoltRequest:
    RequestParsing().process(req=req, resp=BoltResponse(status=200), next=lambda: BoltResponse(status=200))
    return req
