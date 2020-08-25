from logging import Logger
from typing import Optional, Tuple

from slack_bolt.auth import AuthorizationResult


class BaseContext(dict):
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
    def matches(self) -> Optional[Tuple]:
        """Returns all the matched parts in message listener's regexp"""
        return self.get("matches", None)
