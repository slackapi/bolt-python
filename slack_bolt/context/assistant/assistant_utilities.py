from typing import Optional

from slack_sdk.web import WebClient
from slack_bolt.context.assistant.thread_context_store.store import AssistantThreadContextStore
from slack_bolt.context.assistant.thread_context_store.default_store import DefaultAssistantThreadContextStore


from slack_bolt.context.context import BoltContext
from slack_bolt.context.say import Say
from .internals import has_channel_id_and_thread_ts
from ..get_thread_context.get_thread_context import GetThreadContext
from ..save_thread_context import SaveThreadContext
from ..set_status import SetStatus
from ..set_suggested_prompts import SetSuggestedPrompts
from ..set_title import SetTitle


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

        if has_channel_id_and_thread_ts(self.payload):
            # assistant_thread_started
            thread = self.payload["assistant_thread"]
            self.channel_id = thread["channel_id"]
            self.thread_ts = thread["thread_ts"]
        elif self.payload.get("channel") is not None and self.payload.get("thread_ts") is not None:
            # message event
            self.channel_id = self.payload["channel"]
            self.thread_ts = self.payload["thread_ts"]
        else:
            # When moving this code to Bolt internals, no need to raise an exception for this pattern
            raise ValueError(f"Cannot instantiate Assistant for this event pattern ({self.payload})")

    def is_valid(self) -> bool:
        return self.channel_id is not None and self.thread_ts is not None

    @property
    def set_status(self) -> SetStatus:
        return SetStatus(self.client, self.channel_id, self.thread_ts)

    @property
    def set_title(self) -> SetTitle:
        return SetTitle(self.client, self.channel_id, self.thread_ts)

    @property
    def set_suggested_prompts(self) -> SetSuggestedPrompts:
        return SetSuggestedPrompts(self.client, self.channel_id, self.thread_ts)

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
