from typing import Dict, List, Optional, Sequence, Union

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse


class AsyncSetSuggestedPrompts:
    client: AsyncWebClient
    channel_id: str
    thread_ts: Optional[str]

    def __init__(
        self,
        client: AsyncWebClient,
        channel_id: str,
        thread_ts: Optional[str] = None,
    ):
        self.client = client
        self.channel_id = channel_id
        self.thread_ts = thread_ts

    async def __call__(
        self,
        prompts: Sequence[Union[str, Dict[str, str]]],
        title: Optional[str] = None,
        thread_ts: Optional[str] = None,
    ) -> AsyncSlackResponse:
        prompts_arg: List[Dict[str, str]] = []
        for prompt in prompts:
            if isinstance(prompt, str):
                prompts_arg.append({"title": prompt, "message": prompt})
            else:
                prompts_arg.append(prompt)

        return await self.client.assistant_threads_setSuggestedPrompts(
            channel_id=self.channel_id,
            thread_ts=thread_ts or self.thread_ts,
            prompts=prompts_arg,
            title=title,
        )
