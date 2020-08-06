from typing import List, Optional, Union

from slack_bolt.context.ack.internals import _set_response
from slack_bolt.response.response import BoltResponse
from slack_sdk.models.blocks import Block


class Ack:
    response: Optional[BoltResponse]

    def __init__(self):
        self.response: Optional[BoltResponse] = None

    def __call__(
        self,
        text_or_whole_response: Union[str, dict] = "",
        blocks: Optional[List[Union[dict, Block]]] = None,
    ) -> BoltResponse:
        return _set_response(self, text_or_whole_response, blocks)
