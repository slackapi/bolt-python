from typing import Callable

from slack_bolt.context.base_context import BaseContext
from slack_bolt.middleware.middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class RequestParsing(Middleware):
    """Parses the body and builds the context of a request created with `defer_parsing=True`.

    Runs right after `RequestVerification`, so unsigned payloads are never parsed.
    """

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if req.defer_parsing:
            req.complete_deferred_parsing()
            attach_team_id_to_client(req.context)
        return next()


def attach_team_id_to_client(context: BaseContext) -> None:
    if context.team_id is not None and context.get("client") is not None:
        context["client"].default_params["team_id"] = context.team_id
