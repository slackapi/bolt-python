import re
from typing import Callable, Pattern, Union

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.middleware.middleware import Middleware


class FunctionListenerToken(Middleware):  # type: ignore

    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        # As this method is not supposed to be invoked by bolt-python users,
        # the naming conflict with the built-in one affects
        # only the internals of this method
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        if req.context.bot_access_token:
            req.context.client.token = req.context.bot_access_token
            return next()

        # As the text doesn't match, skip running the listener
        return resp
