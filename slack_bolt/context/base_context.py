from logging import Logger
from typing import Optional, Tuple

from slack_bolt.authorization import AuthorizeResult


class BaseContext(dict):
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
    def is_enterprise_install(self) -> Optional[bool]:
        return self.get("is_enterprise_install")

    @property
    def team_id(self) -> Optional[str]:
        return self.get("team_id")

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

    # --------------------------------

    @property
    def authorize_result(self) -> Optional[AuthorizeResult]:
        return self.get("authorize_result")

    @property
    def bot_token(self) -> Optional[str]:
        return self.get("bot_token")

    @property
    def bot_id(self) -> Optional[str]:
        return self.get("bot_id")

    @property
    def bot_user_id(self) -> Optional[str]:
        return self.get("bot_user_id")

    @property
    def user_token(self) -> Optional[str]:
        return self.get("user_token")

    def set_authorize_result(self, authorize_result: AuthorizeResult):
        self["authorize_result"] = authorize_result
        if authorize_result.bot_id is not None:
            self["bot_id"] = authorize_result.bot_id
        if authorize_result.bot_user_id is not None:
            self["bot_user_id"] = authorize_result.bot_user_id
        if authorize_result.bot_token is not None:
            self["bot_token"] = authorize_result.bot_token
        if authorize_result.user_id is not None:
            self["user_id"] = authorize_result.user_id
        if authorize_result.user_token is not None:
            self["user_token"] = authorize_result.user_token
