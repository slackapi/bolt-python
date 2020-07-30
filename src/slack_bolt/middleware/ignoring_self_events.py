import logging
from typing import Callable, Awaitable

from slack_bolt.auth import AuthorizationResult
from slack_bolt.logger import get_bolt_logger
from slack_bolt.request import BoltRequest
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from .async_middleware import AsyncMiddleware
from .middleware import Middleware


class IgnoringSelfEvents(Middleware, AsyncMiddleware):
    def __init__(self):
        self.logger = get_bolt_logger(IgnoringSelfEvents)

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        auth_result = req.context.authorization_result
        if self._is_self_event(auth_result, req.context.user_id):
            self._debug_log(req.payload)
            return req.context.ack()
        else:
            return next()

    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        auth_result = req.context.authorization_result
        if self._is_self_event(auth_result, req.context.user_id):
            self._debug_log(req.payload)
            return await req.context.ack()
        else:
            return await next()

    # -----------------------------------------

    @staticmethod
    def _is_self_event(auth_result: AuthorizationResult, user_id: str):
        return auth_result is not None and user_id == auth_result.bot_user_id

    def _debug_log(self, payload: dict):
        if self.logger.level <= logging.DEBUG:
            event = payload["event"]
            self.logger.debug(f"Skipped self event: {event}")
