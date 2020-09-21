# pytype: skip-file
import logging
from logging import Logger
from typing import Callable, Dict, Any, Optional

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
    body: Dict[str, Any]
    # payload
    payload: Dict[str, Any]
    options: Optional[Dict[str, Any]]  # payload alias
    shortcut: Optional[Dict[str, Any]]  # payload alias
    action: Optional[Dict[str, Any]]  # payload alias
    view: Optional[Dict[str, Any]]  # payload alias
    command: Optional[Dict[str, Any]]  # payload alias
    event: Optional[Dict[str, Any]]  # payload alias
    message: Optional[Dict[str, Any]]  # payload alias
    # utilities
    ack: Ack
    say: Say
    respond: Respond
    # middleware
    next: Callable[[], None]

    def __init__(
        self,
        *,
        logger: logging.Logger,
        client: WebClient,
        req: BoltRequest,
        resp: BoltResponse,
        context: BoltContext,
        body: Dict[str, Any],
        payload: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None,
        shortcut: Optional[Dict[str, Any]] = None,
        action: Optional[Dict[str, Any]] = None,
        view: Optional[Dict[str, Any]] = None,
        command: Optional[Dict[str, Any]] = None,
        event: Optional[Dict[str, Any]] = None,
        message: Optional[Dict[str, Any]] = None,
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

        self.body: Dict[str, Any] = body
        self.payload: Dict[str, Any] = payload
        self.options: Optional[Dict[str, Any]] = options
        self.shortcut: Optional[Dict[str, Any]] = shortcut
        self.action: Optional[Dict[str, Any]] = action
        self.view: Optional[Dict[str, Any]] = view
        self.command: Optional[Dict[str, Any]] = command
        self.event: Optional[Dict[str, Any]] = event
        self.message: Optional[Dict[str, Any]] = message

        self.ack: Ack = ack
        self.say: Say = say
        self.respond: Respond = respond
        self.next: Callable[[], None] = next
