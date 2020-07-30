from typing import Optional, List

from slack_sdk.webhook import AsyncWebhookClient, WebhookResponse


class AsyncRespond():
    def __init__(
        self,
        *,
        response_url: Optional[str]
    ):
        self.response_url: Optional[str] = response_url

    async def __call__(
        self,
        text: str = None,
        blocks: Optional[List[dict]] = None,
        response_type: Optional[str] = None,
        replace_original: Optional[bool] = None,
        delete_original: Optional[bool] = None,
    ) -> WebhookResponse:
        if self.response_url is not None:
            client = AsyncWebhookClient(self.response_url)
            message = {"text": text}
            if blocks is not None:
                message["blocks"] = blocks
            if response_type is not None:
                message["response_type"] = response_type
            if replace_original is not None:
                message["replace_original"] = replace_original
            if delete_original is not None:
                message["delete_original"] = delete_original
            return await client.send_dict(message)
        else:
            raise ValueError("respond is unsupported here as there is no response_url")
