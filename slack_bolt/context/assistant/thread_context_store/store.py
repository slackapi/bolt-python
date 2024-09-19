from typing import Dict, Optional

from slack_bolt.context.assistant.thread_context import AssistantThreadContext


class AssistantThreadContextStore:
    def save(self, *, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None:
        raise NotImplementedError()

    def find(self, *, channel_id: str, thread_ts: str) -> Optional[AssistantThreadContext]:
        raise NotImplementedError()
