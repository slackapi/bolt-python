from typing import List, Dict, Union, Optional

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


class SetSuggestedPrompts:
    client: WebClient
    channel_id: str
    thread_ts: str

    def __init__(
        self,
        client: WebClient,
        channel_id: str,
        thread_ts: str,
    ):
        self.client = client
        self.channel_id = channel_id
        self.thread_ts = thread_ts

    def __call__(
        self,
        prompts: List[Union[str, Dict[str, str]]],
        title: Optional[str] = None,
    ) -> SlackResponse:
        prompts_arg: List[Dict[str, str]] = []
        for prompt in prompts:
            if isinstance(prompt, str):
                prompts_arg.append({"title": prompt, "message": prompt})
            else:
                prompts_arg.append(prompt)

        return self.client.assistant_threads_setSuggestedPrompts(
            channel_id=self.channel_id,
            thread_ts=self.thread_ts,
            prompts=prompts_arg,
            title=title,
        )
