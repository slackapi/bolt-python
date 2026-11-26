from typing import Awaitable, Callable

from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.middleware.request_parsing.request_parsing import attach_team_id_to_client
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncRequestParsing(AsyncMiddleware):
    """Parses the body and builds the context of a request created with `defer_parsing=True`.

    Runs right after `AsyncRequestVerification`, so unsigned payloads are never parsed.
    """

    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        if req.defer_parsing:
            req.complete_deferred_parsing()
            attach_team_id_to_client(req.context)
        return await next()
