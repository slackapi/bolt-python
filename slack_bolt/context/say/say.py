from typing import Callable, Dict, Optional, Sequence, Union

from slack_sdk import WebClient
from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block
from slack_sdk.models.metadata import Metadata
from slack_sdk.web import SlackResponse

from slack_bolt.context.say.internals import _can_say
from slack_bolt.util.utils import create_copy


class Say:
    client: Optional[WebClient]
    channel: Optional[str]
    thread_ts: Optional[str]
    metadata: Optional[Union[Dict, Metadata]]
    build_metadata: Optional[Callable[[], Optional[Union[Dict, Metadata]]]]

    def __init__(
        self,
        client: Optional[WebClient],
        channel: Optional[str],
        thread_ts: Optional[str] = None,
        metadata: Optional[Union[Dict, Metadata]] = None,
        build_metadata: Optional[Callable[[], Optional[Union[Dict, Metadata]]]] = None,
    ):
        self.client = client
        self.channel = channel
        self.thread_ts = thread_ts
        self.metadata = metadata
        self.build_metadata = build_metadata

    def __call__(
        self,
        text: Union[str, dict] = "",
        blocks: Optional[Sequence[Union[Dict, Block]]] = None,
        attachments: Optional[Sequence[Union[Dict, Attachment]]] = None,
        channel: Optional[str] = None,
        as_user: Optional[bool] = None,
        thread_ts: Optional[str] = None,
        reply_broadcast: Optional[bool] = None,
        unfurl_links: Optional[bool] = None,
        unfurl_media: Optional[bool] = None,
        icon_emoji: Optional[str] = None,
        icon_url: Optional[str] = None,
        username: Optional[str] = None,
        markdown_text: Optional[str] = None,
        mrkdwn: Optional[bool] = None,
        link_names: Optional[bool] = None,
        parse: Optional[str] = None,  # none, full
        metadata: Optional[Union[Dict, Metadata]] = None,
        **kwargs,
    ) -> SlackResponse:
        if _can_say(self, channel):
            text_or_whole_response: Union[str, dict] = text
            if isinstance(text_or_whole_response, str):
                text = text_or_whole_response
                if metadata is None:
                    metadata = self.build_metadata() if self.build_metadata is not None else self.metadata
                return self.client.chat_postMessage(  # type: ignore[union-attr]
                    channel=channel or self.channel,  # type: ignore[arg-type]
                    text=text,
                    blocks=blocks,
                    attachments=attachments,
                    as_user=as_user,
                    thread_ts=thread_ts or self.thread_ts,
                    reply_broadcast=reply_broadcast,
                    unfurl_links=unfurl_links,
                    unfurl_media=unfurl_media,
                    icon_emoji=icon_emoji,
                    icon_url=icon_url,
                    username=username,
                    markdown_text=markdown_text,
                    mrkdwn=mrkdwn,
                    link_names=link_names,
                    parse=parse,
                    metadata=metadata,
                    **kwargs,
                )
            elif isinstance(text_or_whole_response, dict):
                message: dict = create_copy(text_or_whole_response)
                if "channel" not in message:
                    message["channel"] = channel or self.channel
                if "thread_ts" not in message:
                    message["thread_ts"] = thread_ts or self.thread_ts
                if "metadata" not in message:
                    metadata = self.build_metadata() if self.build_metadata is not None else self.metadata
                    message["metadata"] = metadata
                return self.client.chat_postMessage(**message)  # type: ignore[union-attr]
            else:
                raise ValueError(f"The arg is unexpected type ({type(text_or_whole_response)})")
        else:
            raise ValueError("say without channel_id here is unsupported")
