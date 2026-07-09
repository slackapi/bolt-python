from typing import Optional, Callable

from slack_bolt.context.assistant.thread_context_store.store import AssistantThreadContextStore
from slack_bolt.context.say_stream.say_stream import SayStream
from slack_bolt.context.set_status.set_status import SetStatus
from slack_bolt.context.set_suggested_prompts.set_suggested_prompts import SetSuggestedPrompts
from slack_bolt.middleware import Middleware
from slack_bolt.context.assistant.assistant_utilities import AssistantUtilities
from slack_bolt.request.payload_utils import (
    is_app_home_opened_event,
    is_assistant_event,
    is_assistant_thread_context_changed_event,
    is_assistant_thread_started_event,
    is_im_message_event,
    to_event,
)
from slack_bolt.request.request import BoltRequest
from slack_bolt.response.response import BoltResponse


class AttachingConversationKwargs(Middleware):

    thread_context_store: Optional[AssistantThreadContextStore]

    def __init__(self, thread_context_store: Optional[AssistantThreadContextStore] = None):
        self.thread_context_store = thread_context_store

    def process(self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse]) -> Optional[BoltResponse]:
        event = to_event(req.body)
        if event is None:
            return next()
        if req.context.channel_id is None:
            return next()

        if is_assistant_event(req.body):
            # TODO: eventually we might remove this assistant specific logic
            assistant = AssistantUtilities(
                payload=event,
                context=req.context,
                thread_context_store=self.thread_context_store,
            )
            req.context["say"] = assistant.say
            req.context["set_title"] = assistant.set_title
            req.context["get_thread_context"] = assistant.get_thread_context
            req.context["save_thread_context"] = assistant.save_thread_context

        if (
            is_im_message_event(req.body)
            or is_assistant_thread_started_event(req.body)
            or is_assistant_thread_context_changed_event(req.body)
            or is_app_home_opened_event(req.body, tab="messages")
        ):
            req.context["set_suggested_prompts"] = SetSuggestedPrompts(
                client=req.context.client,
                channel_id=req.context.channel_id,
                thread_ts=req.context.thread_ts,
            )

        # TODO: in the future we might want to introduce a "proper" extract_ts utility
        thread_ts_or_ts = req.context.thread_ts or event.get("ts")
        if thread_ts_or_ts:
            req.context["set_status"] = SetStatus(
                client=req.context.client,
                channel_id=req.context.channel_id,
                thread_ts=thread_ts_or_ts,
            )
            req.context["say_stream"] = SayStream(
                client=req.context.client,
                channel=req.context.channel_id,
                recipient_team_id=req.context.team_id or req.context.enterprise_id,
                recipient_user_id=req.context.user_id,
                thread_ts=thread_ts_or_ts,
            )
        return next()
