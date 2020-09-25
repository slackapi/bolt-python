from logging import Logger
from typing import Optional, Tuple

from slack_bolt.authorization import AuthorizeResult


class BaseContext(dict):
    @property
    def authorize_result(self) -> Optional[AuthorizeResult]:
        return self.get("authorize_result")

    @property
    def logger(self) -> Logger:
        return self["logger"]

    @property
    def token(self) -> Optional[str]:
        return self.get("token")

    @property
    def enterprise_id(self) -> Optional[str]:
        return self.get("enterprise_id")

    @property
    def team_id(self) -> str:
        return self["team_id"]

    @property
    def user_id(self) -> Optional[str]:
        return self.get("user_id")

    @property
    def channel_id(self) -> Optional[str]:
        return self.get("channel_id")

    @property
    def response_url(self) -> Optional[str]:
        return self.get("response_url")

    @property
    def matches(self) -> Optional[Tuple]:
        """Returns all the matched parts in message listener's regexp"""
        return self.get("matches")
