from typing import Callable, Awaitable

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.middleware.async_middleware import AsyncMiddleware


class AsyncAttachingFunctionToken(AsyncMiddleware):
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        # This method is not supposed to be invoked by bolt-python users
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        if req.context.function_bot_access_token is not None:
            req.context.client.token = req.context.function_bot_access_token  # type: ignore[union-attr]

        return await next()
