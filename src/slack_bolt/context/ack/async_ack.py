from typing import List, Optional, Union

from slack_bolt.context.ack.internals import _set_response
from slack_bolt.response.response import BoltResponse
from slack_sdk.models.block_kit import Block


class AsyncAck:
    response: Optional[BoltResponse]

    def __init__(self):
        self.response: Optional[BoltResponse] = None

    async def __call__(
        self, text: str = "", blocks: Optional[List[Union[dict, Block]]] = None,
    ) -> BoltResponse:
        return _set_response(self, text, blocks)
