import json
from typing import Optional, Dict, Union, Any, Sequence
from urllib.parse import parse_qsl, parse_qs

from slack_bolt.context import BoltContext


def parse_query(
    query: Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]]
) -> Dict[str, Sequence[str]]:
    if query is None:
        return {}
    elif isinstance(query, str):
        return parse_qs(query)
    elif isinstance(query, dict) or hasattr(query, "items"):
        result: Dict[str, Sequence[str]] = {}
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
        if "payload" in body:  # This is not JSON format yet
            params = dict(parse_qsl(body))
            if params.get("payload") is not None:
                return json.loads(params.get("payload"))
            else:
                return {}
        else:
            return dict(parse_qsl(body))


def extract_is_enterprise_install(payload: Dict[str, Any]) -> Optional[bool]:
    if payload.get("authorizations") is not None and len(payload["authorizations"]) > 0:
        # To make Events API handling functioning also for shared channels,
        # we should use .authorizations[0].is_enterprise_install over .is_enterprise_install
        return extract_is_enterprise_install(payload["authorizations"][0])
    if "is_enterprise_install" in payload:
        is_enterprise_install = payload.get("is_enterprise_install")
        return is_enterprise_install is not None and (
            is_enterprise_install is True or is_enterprise_install == "true"
        )
    return False


def extract_enterprise_id(payload: Dict[str, Any]) -> Optional[str]:
    if payload.get("enterprise") is not None:
        org = payload.get("enterprise")
        if isinstance(org, str):
            return org
        elif "id" in org:
            return org.get("id")  # type: ignore
    if payload.get("authorizations") is not None and len(payload["authorizations"]) > 0:
        # To make Events API handling functioning also for shared channels,
        # we should use .authorizations[0].enterprise_id over .enterprise_id
        return extract_enterprise_id(payload["authorizations"][0])
    if "enterprise_id" in payload:
        return payload.get("enterprise_id")
    if payload.get("team") is not None and "enterprise_id" in payload["team"]:
        # In the case where the type is view_submission
        return payload["team"].get("enterprise_id")
    if payload.get("event") is not None:
        return extract_enterprise_id(payload["event"])
    return None


def extract_team_id(payload: Dict[str, Any]) -> Optional[str]:
    if payload.get("team") is not None:
        # With org-wide installations, payload.team in interactivity payloads can be None
        # You need to extract either payload.user.team_id or payload.view.team_id as below
        team = payload.get("team")
        if isinstance(team, str):
            return team
        elif team and "id" in team:
            return team.get("id")
    if payload.get("authorizations") is not None and len(payload["authorizations"]) > 0:
        # To make Events API handling functioning also for shared channels,
        # we should use .authorizations[0].team_id over .team_id
        return extract_team_id(payload["authorizations"][0])
    if "team_id" in payload:
        return payload.get("team_id")
    if payload.get("event") is not None:
        return extract_team_id(payload["event"])
    if payload.get("user") is not None:
        return payload.get("user")["team_id"]
    if payload.get("view") is not None:
        return payload.get("view")["team_id"]
    return None


def extract_user_id(payload: Dict[str, Any]) -> Optional[str]:
    if payload.get("user") is not None:
        user = payload.get("user")
        if isinstance(user, str):
            return user
        elif "id" in user:
            return user.get("id")  # type: ignore
    if "user_id" in payload:
        return payload.get("user_id")
    if payload.get("event") is not None:
        return extract_user_id(payload["event"])
    return None


def extract_channel_id(payload: Dict[str, Any]) -> Optional[str]:
    if payload.get("channel") is not None:
        channel = payload.get("channel")
        if isinstance(channel, str):
            return channel
        elif "id" in channel:
            return channel.get("id")  # type: ignore
    if "channel_id" in payload:
        return payload.get("channel_id")
    if payload.get("event") is not None:
        return extract_channel_id(payload["event"])
    if payload.get("item") is not None:
        # reaction_added: body["event"]["item"]
        return extract_channel_id(payload["item"])
    return None


def build_context(context: BoltContext, body: Dict[str, Any]) -> BoltContext:
    context["is_enterprise_install"] = extract_is_enterprise_install(body)
    enterprise_id = extract_enterprise_id(body)
    if enterprise_id:
        context["enterprise_id"] = enterprise_id
    team_id = extract_team_id(body)
    if team_id:
        context["team_id"] = team_id
    user_id = extract_user_id(body)
    if user_id:
        context["user_id"] = user_id
    channel_id = extract_channel_id(body)
    if channel_id:
        context["channel_id"] = channel_id
    if "response_url" in body:
        context["response_url"] = body["response_url"]
    elif "response_urls" in body:
        # In the case where response_url_enabled: true in a modal exists
        response_urls = body["response_urls"]
        if len(response_urls) >= 1:
            if len(response_urls) > 1:
                context.logger.debug(debug_multiple_response_urls_detected())
            response_url = response_urls[0].get("response_url")
            context["response_url"] = response_url
    return context


def extract_content_type(headers: Dict[str, Sequence[str]]) -> Optional[str]:
    content_type: Optional[str] = headers.get("content-type", [None])[0]
    if content_type:
        return content_type.split(";")[0]
    return None


def build_normalized_headers(
    headers: Optional[Dict[str, Union[str, Sequence[str]]]]
) -> Dict[str, Sequence[str]]:
    normalized_headers: Dict[str, Sequence[str]] = {}
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


def error_message_raw_body_required_in_http_mode() -> str:
    return "`body` must be a raw string data when running in the HTTP server mode"


def debug_multiple_response_urls_detected() -> str:
    return (
        "`response_urls` in the body has multiple URLs in it. "
        "If you would like to use non-primary one, "
        "please manually extract the one from body['response_urls']."
    )
