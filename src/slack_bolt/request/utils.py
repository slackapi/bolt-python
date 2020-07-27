import json
from typing import Optional
from urllib.parse import parse_qsl


def parse_payload(body: str, content_type: Optional[str]) -> dict:
    if not body:
        return {}
    if content_type == "application/json" or body.startswith("{"):
        return json.loads(body)
    elif content_type == "application/x-www-form-urlencoded":
        if "payload" in body:
            params = dict(parse_qsl(body))
            if "payload" in params:
                return json.loads(params.get("payload"))
            else:
                return {}
        else:
            return dict(parse_qsl(body))
    else:
        return {}


def extract_enterprise_id(payload: dict):
    if "enterprise" in payload:
        org = payload.get("enterprise")
        if isinstance(org, str):
            return org
        elif "id" in org:
            return org.get("id")
    if "enterprise_id" in payload:
        return payload.get("enterprise_id")
    if "event" in payload:
        return extract_enterprise_id(payload["event"])
    return None


def extract_team_id(payload: dict):
    if "team" in payload:
        team = payload.get("team")
        if isinstance(team, str):
            return team
        elif "id" in team:
            return team.get("id")
    if "team_id" in payload:
        return payload.get("team_id")
    if "event" in payload:
        return extract_team_id(payload["event"])
    return None


def extract_user_id(payload: dict):
    if "user" in payload:
        user = payload.get("user")
        if isinstance(user, str):
            return user
        elif "id" in user:
            return user.get("id")
    if "user_id" in payload:
        return payload.get("user_id")
    if "event" in payload:
        return extract_user_id(payload["event"])
    return None


def extract_channel_id(payload: dict):
    if "channel" in payload:
        channel = payload.get("channel")
        if isinstance(channel, str):
            return channel
        elif "id" in channel:
            return channel.get("id")
    if "channel_id" in payload:
        return payload.get("channel_id")
    if "event" in payload:
        return extract_channel_id(payload["event"])
    return None
