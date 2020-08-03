from typing import Optional, List

from slack_bolt.context.respond.internals import _build_message
from slack_sdk.webhook.async_client import AsyncWebhookClient, WebhookResponse


class AsyncRespond:
    response_url: Optional[str]

    def __init__(self, *, response_url: Optional[str]):
        self.response_url: Optional[str] = response_url

    async def __call__(
        self,
        text: str = "",
        blocks: Optional[List[dict]] = None,
        response_type: Optional[str] = None,
        replace_original: Optional[bool] = None,
        delete_original: Optional[bool] = None,
    ) -> WebhookResponse:
        if self.response_url is not None:
            client = AsyncWebhookClient(self.response_url)
            message = _build_message(
                text=text,
                blocks=blocks,
                response_type=response_type,
                replace_original=replace_original,
                delete_original=delete_original,
            )
            return await client.send_dict(message)
        else:
            raise ValueError("respond is unsupported here as there is no response_url")
