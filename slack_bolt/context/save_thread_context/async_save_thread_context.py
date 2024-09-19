from typing import Dict

from slack_bolt.context.assistant.thread_context_store.async_store import AsyncAssistantThreadContextStore


class AsyncSaveThreadContext:
    thread_context_store: AsyncAssistantThreadContextStore
    channel_id: str
    thread_ts: str

    def __init__(
        self,
        thread_context_store: AsyncAssistantThreadContextStore,
        channel_id: str,
        thread_ts: str,
    ):
        self.thread_context_store = thread_context_store
        self.channel_id = channel_id
        self.thread_ts = thread_ts

    async def __call__(self, new_context: Dict[str, str]) -> None:
        await self.thread_context_store.save(
            channel_id=self.channel_id,
            thread_ts=self.thread_ts,
            context=new_context,
        )
