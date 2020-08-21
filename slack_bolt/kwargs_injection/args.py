# pytype: skip-file
import logging
from logging import Logger
from typing import Callable, Dict, Any

from slack_bolt.context import BoltContext
from slack_bolt.context.ack import Ack
from slack_bolt.context.respond import Respond
from slack_bolt.context.say import Say
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient


class Args:
    client: WebClient
    logger: Logger
    req: BoltRequest
    resp: BoltResponse
    request: BoltRequest
    response: BoltResponse
    context: BoltContext
    payload: Dict[str, Any]
    ack: Ack
    say: Say
    respond: Respond
    next: Callable[[], None]

    def __init__(
        self,
        *,
        logger: logging.Logger,
        client: WebClient,
        req: BoltRequest,
        resp: BoltResponse,
        context: BoltContext,
        payload: Dict[str, Any],
        ack: Ack,
        say: Say,
        respond: Respond,
        next: Callable[[], None],
        **kwargs  # noqa
    ):
        self.logger: logging.Logger = logger
        self.client: WebClient = client
        self.request = self.req = req
        self.response = self.resp = resp
        self.context: BoltContext = context
        self.payload: Dict[str, Any] = payload
        self.body: Dict[str, Any] = payload
        self.ack: Ack = ack
        self.say: Say = say
        self.respond: Respond = respond
        self.next: Callable[[], None] = next
