from typing import Optional, Callable, Awaitable

from slack_bolt.context.assistant.async_assistant_utilities import AsyncAssistantUtilities
from slack_bolt.context.assistant.thread_context_store.async_store import AsyncAssistantThreadContextStore
from slack_bolt.context.say_stream.async_say_stream import AsyncSayStream
from slack_bolt.context.set_status.async_set_status import AsyncSetStatus
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.request.payload_utils import is_assistant_event, to_event
from slack_bolt.response import BoltResponse


class AsyncAttachingConversationKwargs(AsyncMiddleware):

    thread_context_store: Optional[AsyncAssistantThreadContextStore]

    def __init__(self, thread_context_store: Optional[AsyncAssistantThreadContextStore] = None):
        self.thread_context_store = thread_context_store

    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> Optional[BoltResponse]:
        event = to_event(req.body)
        if event is not None:
            if is_assistant_event(req.body):
                assistant = AsyncAssistantUtilities(
                    payload=event,
                    context=req.context,
                    thread_context_store=self.thread_context_store,
                )
                req.context["say"] = assistant.say
                req.context["set_title"] = assistant.set_title
                req.context["set_suggested_prompts"] = assistant.set_suggested_prompts
                req.context["get_thread_context"] = assistant.get_thread_context
                req.context["save_thread_context"] = assistant.save_thread_context

            # TODO: in the future we might want to introduce a "proper" extract_ts utility
            thread_ts = req.context.thread_ts or event.get("ts")
            if req.context.channel_id and thread_ts:
                req.context["set_status"] = AsyncSetStatus(
                    client=req.context.client,
                    channel_id=req.context.channel_id,
                    thread_ts=thread_ts,
                )
                req.context["say_stream"] = AsyncSayStream(
                    client=req.context.client,
                    channel=req.context.channel_id,
                    recipient_team_id=req.context.team_id or req.context.enterprise_id,
                    recipient_user_id=req.context.user_id,
                    thread_ts=thread_ts,
                )
        return await next()
