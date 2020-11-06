from typing import Optional, Union, Sequence

from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block
from slack_sdk.webhook.async_client import AsyncWebhookClient, WebhookResponse

from slack_bolt.context.respond.internals import _build_message


class AsyncRespond:
    response_url: Optional[str]

    def __init__(self, *, response_url: Optional[str]):
        self.response_url: Optional[str] = response_url

    async def __call__(
        self,
        text: Union[str, dict] = "",
        blocks: Optional[Sequence[Union[dict, Block]]] = None,
        attachments: Optional[Sequence[Union[dict, Attachment]]] = None,
        response_type: Optional[str] = None,
        replace_original: Optional[bool] = None,
        delete_original: Optional[bool] = None,
    ) -> WebhookResponse:
        if self.response_url is not None:
            client = AsyncWebhookClient(self.response_url)
            text_or_whole_response: Union[str, dict] = text
            if isinstance(text_or_whole_response, str):
                message = _build_message(
                    text=text,
                    blocks=blocks,
                    attachments=attachments,
                    response_type=response_type,
                    replace_original=replace_original,
                    delete_original=delete_original,
                )
                return await client.send_dict(message)
            elif isinstance(text_or_whole_response, dict):
                whole_response: dict = text_or_whole_response
                message = _build_message(**whole_response)
                return await client.send_dict(message)
            else:
                raise ValueError(f"The arg is unexpected type ({type(text)})")
        else:
            raise ValueError("respond is unsupported here as there is no response_url")
