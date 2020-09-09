from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.base_context import BaseContext
from slack_bolt.context.respond.async_respond import AsyncRespond
from slack_bolt.context.say.async_say import AsyncSay


class AsyncBoltContext(BaseContext):
    @property
    def client(self) -> Optional[AsyncWebClient]:
        if "client" not in self:
            self["client"] = AsyncWebClient(token=None)
        return self["client"]

    @property
    def ack(self) -> AsyncAck:
        if "ack" not in self:
            self["ack"] = AsyncAck()
        return self["ack"]

    @property
    def say(self) -> AsyncSay:
        if "say" not in self:
            self["say"] = AsyncSay(client=self.client, channel=self.channel_id)
        return self["say"]

    @property
    def respond(self) -> Optional[AsyncRespond]:
        if "respond" not in self:
            self["respond"] = AsyncRespond(response_url=self.response_url)
        return self["respond"]
