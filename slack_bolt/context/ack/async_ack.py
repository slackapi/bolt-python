from typing import List, Optional, Union

from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block, Option, OptionGroup

from slack_bolt.context.ack.internals import _set_response
from slack_bolt.response.response import BoltResponse


class AsyncAck:
    response: Optional[BoltResponse]

    def __init__(self):
        self.response: Optional[BoltResponse] = None

    async def __call__(
        self,
        text: Union[str, dict] = "",  # text: str or whole_response: dict
        blocks: Optional[List[Union[dict, Block]]] = None,
        attachments: Optional[List[Union[dict, Attachment]]] = None,
        options: Optional[List[Union[dict, Option]]] = None,
        option_groups: Optional[List[Union[dict, OptionGroup]]] = None,
    ) -> BoltResponse:
        return _set_response(
            self,
            text_or_whole_response=text,
            blocks=blocks,
            attachments=attachments,
            options=options,
            option_groups=option_groups,
        )
