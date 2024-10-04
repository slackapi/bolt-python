from typing import Callable, Awaitable

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from .ignoring_self_events import IgnoringSelfEvents
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.payload_utils import is_bot_message_event_in_assistant_thread


class AsyncIgnoringSelfEvents(IgnoringSelfEvents, AsyncMiddleware):
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        auth_result = req.context.authorize_result
        # message events can have $.event.bot_id while it does not have its user_id
        bot_id = req.body.get("event", {}).get("bot_id")
        if self._is_self_event(auth_result, req.context.user_id, bot_id, req.body):  # type: ignore[arg-type]
            if self.ignoring_self_assistant_message_events_enabled is False:
                if is_bot_message_event_in_assistant_thread(req.body):
                    # Assistant#bot_message handler acknowledges this pattern
                    return await next()

            self._debug_log(req.body)
            return await req.context.ack()
        else:
            return await next()
