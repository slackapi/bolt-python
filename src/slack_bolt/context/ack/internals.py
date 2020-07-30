from typing import Optional, List, Union

from slack_bolt.response import BoltResponse
from slack_sdk.models.block_kit import Block


def _set_response(
    self: any,
    text: str = "",
    blocks: Optional[List[Union[dict, Block]]] = None,
) -> BoltResponse:
    if not text and (not blocks or len(blocks) == 0):
        self.response = BoltResponse(status=200, body="")
    else:
        self.response = BoltResponse(
            status=200,
            body={
                "text": text,
                "blocks": blocks,
            }
        )
    return self.response
