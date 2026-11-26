from typing import Awaitable, Callable

from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.middleware.request_parsing.request_parsing import attach_team_id_to_client
from slack_bolt.request.async_internals import build_async_context
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.request.internals import parse_body
from slack_bolt.response import BoltResponse


class AsyncRequestParsing(AsyncMiddleware):
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        if req.raw_body:
            req.body = parse_body(req.raw_body, req.content_type)
        set_before_parsing = dict(req.context)
        build_async_context(req.context, req.body)
        req.context.update(set_before_parsing)
        attach_team_id_to_client(req.context)
        return await next()
