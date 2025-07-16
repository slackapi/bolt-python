from typing import Optional

from slack_bolt.context.assistant.thread_context import AssistantThreadContext
from slack_bolt.context.assistant.thread_context_store.async_store import AsyncAssistantThreadContextStore


class AsyncGetThreadContext:
    thread_context_store: AsyncAssistantThreadContextStore
    payload: dict
    channel_id: str
    thread_ts: str

    _thread_context: Optional[AssistantThreadContext]
    thread_context_loaded: bool

    def __init__(
        self,
        thread_context_store: AsyncAssistantThreadContextStore,
        channel_id: str,
        thread_ts: str,
        payload: dict,
    ):
        self.thread_context_store = thread_context_store
        self.payload = payload
        self.channel_id = channel_id
        self.thread_ts = thread_ts
        self._thread_context: Optional[AssistantThreadContext] = None
        self.thread_context_loaded = False

    async def __call__(self) -> Optional[AssistantThreadContext]:
        if self.thread_context_loaded is True:
            return self._thread_context

        if self.payload.get("assistant_thread") is not None:
            # assistant_thread_started
            thread = self.payload["assistant_thread"]
            self._thread_context = (
                AssistantThreadContext(thread["context"])
                if thread.get("context", {}).get("channel_id") is not None
                else None
            )
            # for this event, the context will never be changed
            self.thread_context_loaded = True
        elif self.payload.get("channel") is not None and self.payload.get("thread_ts") is not None:
            # message event
            self._thread_context = await self.thread_context_store.find(channel_id=self.channel_id, thread_ts=self.thread_ts)

        return self._thread_context
