from typing import Optional


class AuthorizationResult(dict):
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
        self.enterprise_id = enterprise_id
        self.team_id = team_id
        # bot
        self.bot_user_id = bot_user_id
        self.bot_id = bot_id
        self.bot_token = bot_token
        # user
        self.user_id = user_id
        self.user_token = user_token