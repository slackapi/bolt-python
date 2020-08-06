from typing import Optional, List, Union

from slack_sdk.models.blocks import Block

from slack_bolt.error import BoltError
from slack_bolt.response import BoltResponse


def _set_response(
    self: any,
    text_or_whole_response: Union[str, dict] = "",
    blocks: Optional[List[Union[dict, Block]]] = None,
) -> BoltResponse:
    print(text_or_whole_response)
    if isinstance(text_or_whole_response, str):
        text = text_or_whole_response
        if not text and (not blocks or len(blocks) == 0):
            self.response = BoltResponse(status=200, body="")
        else:
            self.response = BoltResponse(
                status=200, body={"text": text, "blocks": blocks,}
            )
        return self.response
    elif isinstance(text_or_whole_response, dict):
        body = text_or_whole_response
        self.response = BoltResponse(status=200, body=body)
    else:
        raise BoltError(
            f"{text_or_whole_response} (type: {type(text_or_whole_response)}) is unsupported"
        )
