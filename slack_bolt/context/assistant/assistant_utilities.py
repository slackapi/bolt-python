from typing import Optional

from slack_sdk.web import WebClient
from slack_bolt.context.assistant.thread_context_store.store import AssistantThreadContextStore
from slack_bolt.context.assistant.thread_context_store.default_store import DefaultAssistantThreadContextStore


from slack_bolt.context.context import BoltContext
from slack_bolt.context.say import Say
from ..get_thread_context.get_thread_context import GetThreadContext
from ..save_thread_context import SaveThreadContext


class AssistantUtilities:
    payload: dict
    client: WebClient
    channel_id: str
    thread_ts: str
    thread_context_store: AssistantThreadContextStore

    def __init__(
        self,
        *,
        payload: dict,
        context: BoltContext,
        thread_context_store: Optional[AssistantThreadContextStore] = None,
    ):
        self.payload = payload
        self.client = context.client
        self.thread_context_store = thread_context_store or DefaultAssistantThreadContextStore(context)

        if context.channel_id is not None and context.thread_ts is not None:
            self.channel_id = context.channel_id
            self.thread_ts = context.thread_ts
        else:
            # When moving this code to Bolt internals, no need to raise an exception for this pattern
            raise ValueError(f"Cannot instantiate Assistant for this event pattern ({self.payload})")

    @property
    def say(self) -> Say:
        def build_metadata() -> Optional[dict]:
            thread_context = self.get_thread_context()
            if thread_context is not None:
                return {"event_type": "assistant_thread_context", "event_payload": thread_context}
            return None

        return Say(
            self.client,
            channel=self.channel_id,
            thread_ts=self.thread_ts,
            build_metadata=build_metadata,
        )

    @property
    def get_thread_context(self) -> GetThreadContext:
        return GetThreadContext(self.thread_context_store, self.channel_id, self.thread_ts, self.payload)

    @property
    def save_thread_context(self) -> SaveThreadContext:
        return SaveThreadContext(self.thread_context_store, self.channel_id, self.thread_ts)
