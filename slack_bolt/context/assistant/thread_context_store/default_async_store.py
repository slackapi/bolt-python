from typing import Dict, Optional, List

from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.async_context import AsyncBoltContext

from slack_bolt.context.assistant.thread_context import AssistantThreadContext
from slack_bolt.context.assistant.thread_context_store.async_store import (
    AsyncAssistantThreadContextStore,
)


class DefaultAsyncAssistantThreadContextStore(AsyncAssistantThreadContextStore):
    client: AsyncWebClient
    context: AsyncBoltContext

    def __init__(self, context: AsyncBoltContext):
        self.client = context.client
        self.context = context

    async def save(self, *, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None:
        parent_message = await self._retrieve_first_bot_reply(channel_id, thread_ts)
        if parent_message is not None:
            await self.client.chat_update(
                channel=channel_id,
                ts=parent_message["ts"],
                text=parent_message["text"],
                blocks=parent_message["blocks"],
                metadata={
                    "event_type": "assistant_thread_context",
                    "event_payload": context,
                },
            )

    async def find(self, *, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]:
        parent_message = await self._retrieve_first_bot_reply(channel_id, thread_ts)
        if parent_message is not None and parent_message.get("metadata"):
            if bool(parent_message["metadata"]["event_payload"]):
                return AssistantThreadContext(parent_message["metadata"]["event_payload"])
        return None

    async def _retrieve_first_bot_reply(self, channel_id: str, thread_ts: str) -> Optional[dict]:
        messages: List[dict] = (
            await self.client.conversations_replies(
                channel=channel_id,
                ts=thread_ts,
                oldest=thread_ts,
                include_all_metadata=True,
                limit=4,  # 2 should be usually enough but buffer for more robustness
            )
        ).get("messages", [])
        for message in messages:
            if message.get("subtype") is None and message.get("user") == self.context.bot_user_id:
                return message
        return None
