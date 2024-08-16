from typing import Callable

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.middleware.middleware import Middleware


class AttachingFunctionToken(Middleware):
    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        # This method is not supposed to be invoked by bolt-python users
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if req.context.function_bot_access_token is not None:
            req.context.client.token = req.context.function_bot_access_token  # type: ignore[union-attr]

        return next()
