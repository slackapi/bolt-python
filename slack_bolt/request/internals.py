import json
from typing import Optional, Dict, Union, List, Any
from urllib.parse import parse_qsl, parse_qs

from slack_bolt.context import BoltContext


def parse_query(
    query: Optional[Union[str, Dict[str, str], Dict[str, List[str]]]]
) -> Dict[str, List[str]]:
    if query is None:
        return {}
    elif isinstance(query, str):
        return parse_qs(query)
    elif isinstance(query, dict) or hasattr(query, "items"):
        result: Dict[str, List[str]] = {}
        for name, value in query.items():
            if isinstance(value, list):
                result[name] = value
            elif isinstance(value, str):
                result[name] = [value]
            else:
                raise ValueError(
                    f"Unsupported type ({type(value)}) of element in headers ({query})"
                )
        return result  # type: ignore
    else:
        raise ValueError(f"Unsupported type of query detected ({type(query)})")


def parse_body(body: str, content_type: Optional[str]) -> Dict[str, Any]:
    if not body:
        return {}
    if (
        content_type is not None and content_type == "application/json"
    ) or body.startswith("{"):
        return json.loads(body)
    else:
        if "payload" in body:
            params = dict(parse_qsl(body))
            if "payload" in params:
                return json.loads(params.get("payload"))
            else:
                return {}
        else:
            return dict(parse_qsl(body))


def extract_enterprise_id(payload: Dict[str, Any]) -> Optional[str]:
    if "enterprise" in payload:
        org = payload.get("enterprise")
        if isinstance(org, str):
            return org
        elif "id" in org:
            return org.get("id")  # type: ignore
    if "enterprise_id" in payload:
        return payload.get("enterprise_id")
    if "team" in payload and "enterprise_id" in payload["team"]:
        # In the case where the type is view_submission
        return payload["team"].get("enterprise_id")
    if "event" in payload:
        return extract_enterprise_id(payload["event"])
    return None


def extract_team_id(payload: Dict[str, Any]) -> Optional[str]:
    if "team" in payload:
        team = payload.get("team")
        if isinstance(team, str):
            return team
        elif team and "id" in team:
            return team.get("id")
    if "team_id" in payload:
        return payload.get("team_id")
    if "event" in payload:
        return extract_team_id(payload["event"])
    if "user" in payload:
        return payload.get("user")["team_id"]
    return None


def extract_user_id(payload: Dict[str, Any]) -> Optional[str]:
    if "user" in payload:
        user = payload.get("user")
        if isinstance(user, str):
            return user
        elif "id" in user:
            return user.get("id")  # type: ignore
    if "user_id" in payload:
        return payload.get("user_id")
    if "event" in payload:
        return extract_user_id(payload["event"])
    return None


def extract_channel_id(payload: Dict[str, Any]) -> Optional[str]:
    if "channel" in payload:
        channel = payload.get("channel")
        if isinstance(channel, str):
            return channel
        elif "id" in channel:
            return channel.get("id")  # type: ignore
    if "channel_id" in payload:
        return payload.get("channel_id")
    if "event" in payload:
        return extract_channel_id(payload["event"])
    if "item" in payload:
        # reaction_added: body["event"]["item"]
        return extract_channel_id(payload["item"])
    return None


def build_context(context: BoltContext, payload: Dict[str, Any],) -> BoltContext:
    enterprise_id = extract_enterprise_id(payload)
    if enterprise_id:
        context["enterprise_id"] = enterprise_id
    team_id = extract_team_id(payload)
    if team_id:
        context["team_id"] = team_id
    user_id = extract_user_id(payload)
    if user_id:
        context["user_id"] = user_id
    channel_id = extract_channel_id(payload)
    if channel_id:
        context["channel_id"] = channel_id
    if "response_url" in payload:
        context["response_url"] = payload["response_url"]
    return context


def extract_content_type(headers: Dict[str, List[str]]) -> Optional[str]:
    content_type: Optional[str] = headers.get("content-type", [None])[0]
    if content_type:
        return content_type.split(";")[0]
    return None


def build_normalized_headers(
    headers: Optional[Dict[str, Union[str, List[str]]]]
) -> Dict[str, List[str]]:
    normalized_headers: Dict[str, List[str]] = {}
    if headers is not None:
        for key, value in headers.items():
            normalized_name = key.lower()
            if isinstance(value, list):
                normalized_headers[normalized_name] = value
            elif isinstance(value, str):
                normalized_headers[normalized_name] = [value]
            else:
                raise ValueError(
                    f"Unsupported type ({type(value)}) of element in headers ({headers})"
                )
    return normalized_headers  # type: ignore
