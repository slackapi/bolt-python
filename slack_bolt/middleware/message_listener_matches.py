import re
from typing import Callable, Pattern, Union

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .middleware import Middleware


class MessageListenerMatches(Middleware):  # type: ignore
    def __init__(self, keyword: Union[str, Pattern]):
        self.keyword = keyword

    def process(
        self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        text = req.payload.get("event", {}).get("text", "")
        if text:
            m = re.search(self.keyword, text)
            if m is not None:
                req.context["matches"] = m.groups()  # tuple
                return next()

        # As the text doesn't match, skip running the listener
        return resp
