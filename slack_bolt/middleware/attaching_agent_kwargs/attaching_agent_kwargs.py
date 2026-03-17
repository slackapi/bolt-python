from typing import Optional, Callable

from slack_bolt.context.assistant.assistant_utilities import AssistantUtilities
from slack_bolt.context.assistant.thread_context_store.store import AssistantThreadContextStore
from slack_bolt.middleware import Middleware
from slack_bolt.request.payload_utils import is_assistant_event, to_event
from slack_bolt.request.request import BoltRequest
from slack_bolt.response.response import BoltResponse


class AttachingAgentKwargs(Middleware):

    thread_context_store: Optional[AssistantThreadContextStore]

    def __init__(self, thread_context_store: Optional[AssistantThreadContextStore] = None):
        self.thread_context_store = thread_context_store

    def process(self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse]) -> Optional[BoltResponse]:
        event = to_event(req.body)
        if event is not None:
            if is_assistant_event(req.body):
                assistant = AssistantUtilities(
                    payload=event,
                    context=req.context,
                    thread_context_store=self.thread_context_store,
                )
                req.context["say"] = assistant.say
                req.context["set_status"] = assistant.set_status
                req.context["set_title"] = assistant.set_title
                req.context["set_suggested_prompts"] = assistant.set_suggested_prompts
                req.context["get_thread_context"] = assistant.get_thread_context
                req.context["save_thread_context"] = assistant.save_thread_context
        return next()
