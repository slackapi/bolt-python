from typing import Dict, Optional

from slack_bolt.context.assistant.thread_context import AssistantThreadContext


class AsyncAssistantThreadContextStore:
    async def save(self, *, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None:
        raise NotImplementedError()

    async def find(self, *, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]:
        raise NotImplementedError()
