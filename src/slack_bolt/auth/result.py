from typing import Optional


class AuthorizationResult(dict):
    enterprise_id: Optional[str]
    team_id: Optional[str]
    bot_id: str
    bot_user_id: str
    bot_token: str
    user_id: Optional[str]
    user_token: Optional[str]

    def __init__(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        # bot
        bot_user_id: str,
        bot_id: str,
        bot_token: str,
        # user
        user_id: Optional[str] = None,
        user_token: Optional[str] = None,
    ):
        self.enterprise_id: Optional[str] = enterprise_id
        self.team_id: Optional[str] = team_id
        # bot
        self.bot_user_id: str = bot_user_id
        self.bot_id: str = bot_id
        self.bot_token: str = bot_token
        # user
        self.user_id: Optional[str] = user_id
        self.user_token: Optional[str] = user_token
