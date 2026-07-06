from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.context.assistant.thread_context_store.async_store import (
    AsyncAssistantThreadContextStore,
)

from slack_bolt.context.assistant.thread_context_store.default_async_store import DefaultAsyncAssistantThreadContextStore


from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.say.async_say import AsyncSay
from ..get_thread_context.async_get_thread_context import AsyncGetThreadContext
from ..save_thread_context.async_save_thread_context import AsyncSaveThreadContext


class AsyncAssistantUtilities:
    payload: dict
    client: AsyncWebClient
    channel_id: str
    thread_ts: str
    thread_context_store: AsyncAssistantThreadContextStore

    def __init__(
        self,
        *,
        payload: dict,
        context: AsyncBoltContext,
        thread_context_store: Optional[AsyncAssistantThreadContextStore] = None,
    ):
        self.payload = payload
        self.client = context.client
        self.thread_context_store = thread_context_store or DefaultAsyncAssistantThreadContextStore(context)

        if context.channel_id is not None and context.thread_ts is not None:
            self.channel_id = context.channel_id
            self.thread_ts = context.thread_ts
        else:
            # When moving this code to Bolt internals, no need to raise an exception for this pattern
            raise ValueError(f"Cannot instantiate Assistant for this event pattern ({self.payload})")

    @property
    def say(self) -> AsyncSay:
        return AsyncSay(
            self.client,
            channel=self.channel_id,
            thread_ts=self.thread_ts,
            build_metadata=self._build_message_metadata,
        )

    async def _build_message_metadata(self) -> dict:
        return {
            "event_type": "assistant_thread_context",
            "event_payload": await self.get_thread_context(),
        }

    @property
    def get_thread_context(self) -> AsyncGetThreadContext:
        return AsyncGetThreadContext(self.thread_context_store, self.channel_id, self.thread_ts, self.payload)

    @property
    def save_thread_context(self) -> AsyncSaveThreadContext:
        return AsyncSaveThreadContext(self.thread_context_store, self.channel_id, self.thread_ts)
