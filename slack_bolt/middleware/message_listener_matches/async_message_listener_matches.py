import re
from typing import Callable, Awaitable, Union, Pattern

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.middleware.async_middleware import AsyncMiddleware


class AsyncMessageListenerMatches(AsyncMiddleware):
    def __init__(self, keyword: Union[str, Pattern]):
        """Captures matched keywords and saves the values in context."""
        self.keyword = keyword

    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        text = req.body.get("event", {}).get("text", "")
        if text:
            m = re.search(self.keyword, text)
            if m is not None:
                req.context["matches"] = m.groups()  # tuple
                return await next()

        # As the text doesn't match, skip running the listener
        return resp
