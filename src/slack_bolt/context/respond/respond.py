from typing import Optional, List

from slack_sdk.webhook import WebhookClient, WebhookResponse


class Respond():
    def __init__(
        self,
        *,
        response_url: Optional[str]
    ):
        self.response_url = response_url

    def __call__(
        self,
        text: str = None,
        blocks: List[dict] = [],
        response_type: Optional[str] = None,
        replace_original: Optional[bool] = None,
        delete_original: Optional[bool] = None,
    ) -> WebhookResponse:
        if self.response_url:
            client = WebhookClient(self.response_url)
            message = {"text": text, "blocks": blocks, }
            if response_type:
                message["response_type"] = response_type
            if replace_original is not None:
                message["replace_original"] = replace_original
            if delete_original is not None:
                message["delete_original"] = delete_original
            return client.send_dict(message)
        else:
            raise ValueError("respond is unsupported here as there is no response_url")
