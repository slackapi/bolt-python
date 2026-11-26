from typing import Callable

from slack_bolt.context.base_context import BaseContext
from slack_bolt.middleware.middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.request.internals import build_context, parse_body
from slack_bolt.response import BoltResponse


class RequestParsing(Middleware):
    """Parses the request body and builds the context from it.

    Runs right after `RequestVerification`, so unsigned payloads are never parsed.
    Values already in the context take precedence over the ones in the body.
    """

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if req.raw_body:
            req.body = parse_body(req.raw_body, req.content_type)
        set_before_parsing = dict(req.context)
        build_context(req.context, req.body)
        req.context.update(set_before_parsing)
        attach_team_id_to_client(req.context)
        return next()


def attach_team_id_to_client(context: BaseContext) -> None:
    if context.team_id is not None and context.get("client") is not None:
        context["client"].default_params["team_id"] = context.team_id
