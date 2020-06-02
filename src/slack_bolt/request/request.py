from typing import Dict

from slack_bolt.context.context import BoltContext
from slack_bolt.request.utils import \
    parse_payload, \
    extract_enterprise_id, \
    extract_team_id, \
    extract_user_id, \
    extract_channel_id


class BoltRequest():
    def __init__(
        self,
        *,
        body: str,
        headers: Dict[str, str] = {},
        context: Dict[str, any] = {},
    ):
        self.body = body
        self.headers = headers
        self.content_type = headers.get("content-type", None)
        if self.content_type:
            self.content_type = self.content_type.split(";")[0]
        self.payload = parse_payload(self.body, self.content_type)
        self._build_context(self.payload, context)

    def _build_context(self, payload: dict, context: dict):
        self.context = BoltContext(context)
        enterprise_id = extract_enterprise_id(payload)
        if enterprise_id:
            self.context["enterprise_id"] = enterprise_id
        team_id = extract_team_id(payload)
        if team_id:
            self.context["team_id"] = team_id
        user_id = extract_user_id(payload)
        if user_id:
            self.context["user_id"] = user_id
        channel_id = extract_channel_id(payload)
        if channel_id:
            self.context["channel_id"] = channel_id
        if "response_url" in payload:
            self.context["response_url"] = payload["response_url"]
