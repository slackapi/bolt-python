from typing import Callable, Awaitable

from .ssl_check import SslCheck
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncSslCheck(SslCheck, AsyncMiddleware):
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        # As this method is not supposed to be invoked by bolt-python users,
        # the naming conflict with the built-in one affects
        # only the internals of this method
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        form_params = self._parse_form_params(req.raw_body)
        if self._is_ssl_check_request(form_params):
            if self._verify_token_if_needed(form_params):
                return self._build_error_response()
            return self._build_success_response()
        else:
            return await next()
