from typing import Callable, Awaitable

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from .ignoring_self_events import IgnoringSelfEvents
from slack_bolt.middleware.async_middleware import AsyncMiddleware


class AsyncIgnoringSelfEvents(IgnoringSelfEvents, AsyncMiddleware):
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        auth_result = req.context.authorize_result
        user_id = req.context.user_id if req.context.user_id is not None else req.context.bot_user_id
        if self._is_self_event(auth_result, user_id, req.body):
            self._debug_log(req.body)
            return await req.context.ack()
        else:
            return await next()
