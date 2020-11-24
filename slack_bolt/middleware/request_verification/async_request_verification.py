from typing import Callable, Awaitable

from slack_bolt.middleware import RequestVerification
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncRequestVerification(RequestVerification, AsyncMiddleware):
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        if self._can_skip(req.mode, req.body):
            return await next()

        body = req.raw_body
        timestamp = req.headers.get("x-slack-request-timestamp", ["0"])[0]
        signature = req.headers.get("x-slack-signature", [""])[0]
        if self.verifier.is_valid(body, timestamp, signature):
            return await next()
        else:
            self._debug_log_error(signature, timestamp, body)
            return self._build_error_response()
