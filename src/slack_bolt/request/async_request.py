from typing import Dict, Optional, List, Union
from urllib.parse import parse_qs

from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.request.utils import \
    parse_payload, \
    extract_enterprise_id, \
    extract_team_id, \
    extract_user_id, \
    extract_channel_id


class AsyncBoltRequest():
    def __init__(
        self,
        *,
        body: str,
        query: Optional[Union[str, Dict[str, str]]] = None,
        # many framework use Dict[str, str] but the reality is Dict[str, List[str]]
        headers: Optional[Dict[str, Union[str, List[str]]]] = None,
        context: Optional[Dict[str, str]] = None,
    ):
        self.body = body

        if query is None:
            self.query = {}
        elif isinstance(query, str):
            self.query = {k: v[0] for k, v in parse_qs(query).items()}
        else:
            self.query = query

        normalized_headers = {}
        if headers is not None:
            for key, value in headers.items():
                normalized_name = key.lower()
                if isinstance(value, list):
                    normalized_headers[normalized_name] = value
                elif isinstance(value, str):
                    normalized_headers[normalized_name] = [value]
                else:
                    raise ValueError(f"Unsupported type ({type(value)}) of element in headers ({headers})")

        self.headers = normalized_headers
        self.content_type: Optional[str] = normalized_headers.get("content-type", [None])[0]
        if self.content_type:
            self.content_type = self.content_type.split(";")[0]
        self.payload = parse_payload(self.body, self.content_type)
        self._build_context(self.payload, context if context else {})

    def _build_context(self, payload: dict, context: dict):
        self.context = AsyncBoltContext(context)
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
