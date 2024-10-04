from typing import Optional


class AssistantThreadContext(dict):
    enterprise_id: Optional[str]
    team_id: Optional[str]
    channel_id: str

    def __init__(self, payload: dict):
        dict.__init__(self, **payload)
        self.enterprise_id = payload.get("enterprise_id")
        self.team_id = payload.get("team_id")
        self.channel_id = payload["channel_id"]
