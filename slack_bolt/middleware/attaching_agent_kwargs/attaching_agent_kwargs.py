from typing import Callable

from slack_bolt.context.say_stream.say_stream import SayStream
from slack_bolt.context.set_status.set_status import SetStatus
from slack_bolt.context.set_suggested_prompts.set_suggested_prompts import SetSuggestedPrompts
from slack_bolt.context.set_title.set_title import SetTitle
from slack_bolt.middleware.middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class AttachingAgentKwargs(Middleware):
    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        # This method is not supposed to be invoked by bolt-python users
        next: Callable[[], BoltResponse],
    ) -> BoltResponse:
        channel_id = req.context.channel_id
        # TODO: improve the logic around extracting thread_ts and event ts
        event = req.body.get("event", {})
        thread_ts = event.get("thread_ts") or event.get("ts")

        if channel_id and thread_ts:
            client = req.context.client
            req.context["set_status"] = SetStatus(client, channel_id, thread_ts)
            req.context["set_title"] = SetTitle(client, channel_id, thread_ts)
            req.context["set_suggested_prompts"] = SetSuggestedPrompts(client, channel_id, thread_ts)
            req.context["say_stream"] = SayStream(
                client=req.context.client,
                channel_id=channel_id,
                thread_ts=thread_ts,
                team_id=req.context.team_id,
                user_id=req.context.user_id,
            )

        return next()
