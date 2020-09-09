# pytype: skip-file
from typing import Optional

from slack_sdk import WebClient

from slack_bolt.context.ack import Ack
from slack_bolt.context.base_context import BaseContext
from slack_bolt.context.respond import Respond
from slack_bolt.context.say import Say


class BoltContext(BaseContext):
    @property
    def client(self) -> Optional[WebClient]:
        if "client" not in self:
            self["client"] = WebClient(token=None)
        return self["client"]

    @property
    def ack(self) -> Ack:
        if "ack" not in self:
            self["ack"] = Ack()
        return self["ack"]

    @property
    def say(self) -> Say:
        if "say" not in self:
            self["say"] = Say(client=self.client, channel=self.channel_id)
        return self["say"]

    @property
    def respond(self) -> Optional[Respond]:
        if "respond" not in self:
            self["respond"] = Respond(response_url=self.response_url)
        return self["respond"]
