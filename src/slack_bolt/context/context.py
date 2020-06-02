from logging import Logger
from typing import Optional

from slack_bolt.auth import AuthorizationResult
from slack_bolt.context.ack import Ack
from slack_bolt.context.respond import Respond
from slack_bolt.context.say import Say
from slack_sdk import WebClient


class BoltContext(dict):

    @property
    def authorization_result(self) -> Optional[AuthorizationResult]:
        return self.get("authorization_result", None)

    @property
    def logger(self) -> Logger:
        return self["logger"]

    @property
    def token(self) -> Optional[str]:
        return self.get("token", None)

    @property
    def client(self) -> Optional[WebClient]:
        return self.get("client", None)

    @property
    def enterprise_id(self) -> Optional[str]:
        return self.get("enterprise_id", None)

    @property
    def team_id(self) -> str:
        return self["team_id"]

    @property
    def user_id(self) -> Optional[str]:
        return self.get("user_id", None)

    @property
    def channel_id(self) -> Optional[str]:
        return self.get("channel_id", None)

    @property
    def response_url(self) -> Optional[str]:
        return self.get("response_url", None)

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
