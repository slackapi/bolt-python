# pytype: skip-file
from logging import Logger
from typing import Callable, Awaitable, Dict, Any, Optional

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.respond.async_respond import AsyncRespond
from slack_bolt.context.say.async_say import AsyncSay
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from slack_sdk.web.async_client import AsyncWebClient


class AsyncArgs:
    logger: Logger
    client: AsyncWebClient
    req: AsyncBoltRequest
    resp: BoltResponse
    request: AsyncBoltRequest
    response: BoltResponse
    context: AsyncBoltContext
    # payload
    payload: Dict[str, Any]
    options: Optional[Dict[str, Any]]
    shortcut: Optional[Dict[str, Any]]
    action: Optional[Dict[str, Any]]
    view: Optional[Dict[str, Any]]
    command: Optional[Dict[str, Any]]
    event: Optional[Dict[str, Any]]
    message: Optional[Dict[str, Any]]
    # utilities
    ack: AsyncAck
    say: AsyncSay
    respond: AsyncRespond
    # middleware
    next: Callable[[], Awaitable[None]]

    def __init__(
        self,
        *,
        logger: Logger,
        client: AsyncWebClient,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        context: AsyncBoltContext,
        payload: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None,
        shortcut: Optional[Dict[str, Any]] = None,
        action: Optional[Dict[str, Any]] = None,
        view: Optional[Dict[str, Any]] = None,
        command: Optional[Dict[str, Any]] = None,
        event: Optional[Dict[str, Any]] = None,
        message: Optional[Dict[str, Any]] = None,
        ack: AsyncAck,
        say: AsyncSay,
        respond: AsyncRespond,
        next: Callable[[], Awaitable[None]],
        **kwargs  # noqa
    ):
        self.logger: Logger = logger
        self.client: AsyncWebClient = client
        self.request = self.req = req
        self.response = self.resp = resp
        self.context: AsyncBoltContext = context

        self.payload: Dict[str, Any] = payload
        self.body: Dict[str, Any] = payload
        self.options: Optional[Dict[str, Any]] = options
        self.shortcut: Optional[Dict[str, Any]] = shortcut
        self.action: Optional[Dict[str, Any]] = action
        self.view: Optional[Dict[str, Any]] = view
        self.command: Optional[Dict[str, Any]] = command
        self.event: Optional[Dict[str, Any]] = event
        self.message: Optional[Dict[str, Any]] = message

        self.ack: AsyncAck = ack
        self.say: AsyncSay = say
        self.respond: AsyncRespond = respond
        self.next: Callable[[], Awaitable[None]] = next
