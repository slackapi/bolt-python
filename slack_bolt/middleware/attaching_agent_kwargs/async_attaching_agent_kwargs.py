from typing import Callable, Awaitable

from slack_bolt.context.say_stream.async_say_stream import AsyncSayStream
from slack_bolt.context.set_status.async_set_status import AsyncSetStatus
from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from slack_bolt.context.set_title.async_set_title import AsyncSetTitle
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncAttachingAgentKwargs(AsyncMiddleware):
    async def async_process(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        # This method is not supposed to be invoked by bolt-python users
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> BoltResponse:
        channel_id = req.context.channel_id
        # TODO: improve the logic around extracting thread_ts and event ts
        event = req.body.get("event", {})
        thread_ts = event.get("thread_ts") or event.get("ts")

        if channel_id and thread_ts:
            client = req.context.client
            req.context["set_status"] = AsyncSetStatus(client, channel_id, thread_ts)
            req.context["set_title"] = AsyncSetTitle(client, channel_id, thread_ts)
            req.context["set_suggested_prompts"] = AsyncSetSuggestedPrompts(client, channel_id, thread_ts)

        req.context["say_stream"] = AsyncSayStream(
            client=req.context.client,
            channel_id=channel_id,
            thread_ts=thread_ts,
            team_id=req.context.team_id,
            user_id=req.context.user_id,
        )

        return await next()
