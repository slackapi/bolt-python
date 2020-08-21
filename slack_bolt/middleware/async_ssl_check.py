from typing import Callable, Awaitable

from . import SslCheck
from .async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncSslCheck(SslCheck, AsyncMiddleware):
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        if self._is_ssl_check_request(req.payload):
            if self._verify_token_if_needed(req.payload):
                return self._build_error_response()
            return self._build_success_response()
        else:
            return await next()
