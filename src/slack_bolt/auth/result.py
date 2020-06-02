from typing import Optional


class AuthorizationResult(dict):
    def __init__(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: str,
        bot_id: str,
    ):
        self.enterprise_id = enterprise_id
        self.team_id = team_id
        self.user_id = user_id
        self.bot_id = bot_id
