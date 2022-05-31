from typing import Optional

from slack_sdk.web import SlackResponse


class AuthorizeResult(dict):
    """Authorize function call result"""

    enterprise_id: Optional[str]
    team_id: Optional[str]
    bot_id: Optional[str]
    bot_user_id: Optional[str]
    bot_token: Optional[str]
    user_id: Optional[str]
    user_token: Optional[str]

    def __init__(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        # bot
        bot_user_id: Optional[str] = None,
        bot_id: Optional[str] = None,
        bot_token: Optional[str] = None,
        # user
        user_id: Optional[str] = None,
        user_token: Optional[str] = None,
    ):
        """
        Args:
            enterprise_id: Organization ID (Enterprise Grid) starting with `E`
            team_id: Workspace ID starting with `T`
            bot_user_id: Bot user's User ID starting with either `U` or `W`
            bot_id: Bot ID starting with `B`
            bot_token: Bot user access token starting with `xoxb-`
            user_id: The request user ID
            user_token: User access token starting with `xoxp-`
        """
        self["enterprise_id"] = self.enterprise_id = enterprise_id
        self["team_id"] = self.team_id = team_id
        # bot
        self["bot_user_id"] = self.bot_user_id = bot_user_id
        self["bot_id"] = self.bot_id = bot_id
        self["bot_token"] = self.bot_token = bot_token
        # user
        self["user_id"] = self.user_id = user_id
        self["user_token"] = self.user_token = user_token

    @classmethod
    def from_auth_test_response(
        cls,
        *,
        bot_token: Optional[str] = None,
        user_token: Optional[str] = None,
        auth_test_response: SlackResponse,
    ) -> "AuthorizeResult":
        bot_user_id: Optional[str] = (  # type:ignore
            auth_test_response.get("user_id") if auth_test_response.get("bot_id") is not None else None
        )
        user_id: Optional[str] = (  # type:ignore
            auth_test_response.get("user_id") if auth_test_response.get("bot_id") is None else None
        )
        return AuthorizeResult(
            enterprise_id=auth_test_response.get("enterprise_id"),
            team_id=auth_test_response.get("team_id"),
            bot_id=auth_test_response.get("bot_id"),
            bot_user_id=bot_user_id,
            user_id=user_id,
            bot_token=bot_token,
            user_token=user_token,
        )
