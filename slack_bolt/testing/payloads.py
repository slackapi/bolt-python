"""Builders for the request payloads Slack sends to Bolt apps, for use in tests.

Each function returns the payload as a dict. Use them with `BoltTestClient.dispatch()`,
or with `build_request()` to get a signed `BoltRequest`.
"""

import json
import time
import uuid
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from slack_sdk.signature import SignatureVerifier

from .mock_slack_server import DEFAULT_APP_ID, DEFAULT_BOT_USER_ID, DEFAULT_TEAM_ID, DEFAULT_USER_ID

DEFAULT_CHANNEL_ID = "C0000000000"


def _ts() -> str:
    return f"{time.time():.6f}"


def event(
    event: Dict[str, Any],
    *,
    team_id: str = DEFAULT_TEAM_ID,
    api_app_id: str = DEFAULT_APP_ID,
    authorized_user_id: str = DEFAULT_BOT_USER_ID,
    event_id: Optional[str] = None,
) -> Dict[str, Any]:
    """An Events API `event_callback` payload wrapping the given event."""
    event = {"event_ts": _ts(), **event}
    return {
        "token": "verification-token",
        "team_id": team_id,
        "api_app_id": api_app_id,
        "event": event,
        "type": "event_callback",
        "event_id": event_id or f"Ev{uuid.uuid4().hex[:10].upper()}",
        "event_time": int(time.time()),
        "authorizations": [
            {
                "enterprise_id": None,
                "team_id": team_id,
                "user_id": authorized_user_id,
                "is_bot": True,
                "is_enterprise_install": False,
            }
        ],
        "is_ext_shared_channel": False,
    }


def message(
    text: str,
    *,
    user: str = DEFAULT_USER_ID,
    channel: str = DEFAULT_CHANNEL_ID,
    channel_type: str = "channel",
    ts: Optional[str] = None,
    thread_ts: Optional[str] = None,
    team_id: str = DEFAULT_TEAM_ID,
    **event_fields: Any,
) -> Dict[str, Any]:
    """An Events API payload for a `message` event posted by a user."""
    msg: Dict[str, Any] = {
        "type": "message",
        "text": text,
        "user": user,
        "channel": channel,
        "channel_type": channel_type,
        "ts": ts or _ts(),
        "team": team_id,
    }
    if thread_ts is not None:
        msg["thread_ts"] = thread_ts
    msg.update(event_fields)
    return event(msg, team_id=team_id)


def slash_command(
    command: str,
    text: str = "",
    *,
    user_id: str = DEFAULT_USER_ID,
    user_name: str = "test-user",
    channel_id: str = DEFAULT_CHANNEL_ID,
    channel_name: str = "general",
    team_id: str = DEFAULT_TEAM_ID,
    api_app_id: str = DEFAULT_APP_ID,
    response_url: str = "https://hooks.slack.com/commands/T0000000000/1/test",
    trigger_id: str = "111.222.test",
) -> Dict[str, Any]:
    """A slash command payload."""
    return {
        "token": "verification-token",
        "team_id": team_id,
        "team_domain": "test",
        "channel_id": channel_id,
        "channel_name": channel_name,
        "user_id": user_id,
        "user_name": user_name,
        "command": command,
        "text": text,
        "api_app_id": api_app_id,
        "is_enterprise_install": "false",
        "response_url": response_url,
        "trigger_id": trigger_id,
    }


def _interactive_base(
    type: str,
    *,
    user_id: str,
    team_id: str,
    api_app_id: str,
    trigger_id: str,
) -> Dict[str, Any]:
    return {
        "type": type,
        "token": "verification-token",
        "api_app_id": api_app_id,
        "team": {"id": team_id, "domain": "test"},
        "user": {"id": user_id, "username": "test-user", "name": "test-user", "team_id": team_id},
        "enterprise": None,
        "is_enterprise_install": False,
        "trigger_id": trigger_id,
    }


def block_action(
    action_id: str,
    *,
    value: Optional[str] = None,
    block_id: str = "block",
    action_type: str = "button",
    action: Optional[Dict[str, Any]] = None,
    user_id: str = DEFAULT_USER_ID,
    channel_id: str = DEFAULT_CHANNEL_ID,
    team_id: str = DEFAULT_TEAM_ID,
    api_app_id: str = DEFAULT_APP_ID,
    message: Optional[Dict[str, Any]] = None,
    response_url: str = "https://hooks.slack.com/actions/T0000000000/1/test",
    trigger_id: str = "111.222.test",
) -> Dict[str, Any]:
    """A `block_actions` payload for an interaction with a Block Kit element in a message.

    Pass `action` to send a fully custom action object instead of the default button action.
    """
    body = _interactive_base("block_actions", user_id=user_id, team_id=team_id, api_app_id=api_app_id, trigger_id=trigger_id)
    if action is None:
        action = {"type": action_type, "action_id": action_id, "block_id": block_id, "action_ts": _ts()}
        if value is not None:
            action["value"] = value
    body.update(
        {
            "container": {"type": "message", "channel_id": channel_id, "is_ephemeral": False},
            "channel": {"id": channel_id, "name": "general"},
            "message": message or {"type": "message", "text": "", "ts": _ts()},
            "response_url": response_url,
            "actions": [action],
        }
    )
    return body


def shortcut(
    callback_id: str,
    *,
    user_id: str = DEFAULT_USER_ID,
    team_id: str = DEFAULT_TEAM_ID,
    api_app_id: str = DEFAULT_APP_ID,
    trigger_id: str = "111.222.test",
) -> Dict[str, Any]:
    """A global shortcut payload."""
    body = _interactive_base("shortcut", user_id=user_id, team_id=team_id, api_app_id=api_app_id, trigger_id=trigger_id)
    body.update({"callback_id": callback_id, "action_ts": _ts()})
    return body


def message_shortcut(
    callback_id: str,
    *,
    message: Optional[Dict[str, Any]] = None,
    user_id: str = DEFAULT_USER_ID,
    channel_id: str = DEFAULT_CHANNEL_ID,
    team_id: str = DEFAULT_TEAM_ID,
    api_app_id: str = DEFAULT_APP_ID,
    response_url: str = "https://hooks.slack.com/app/T0000000000/1/test",
    trigger_id: str = "111.222.test",
) -> Dict[str, Any]:
    """A message shortcut payload."""
    body = _interactive_base(
        "message_action", user_id=user_id, team_id=team_id, api_app_id=api_app_id, trigger_id=trigger_id
    )
    body.update(
        {
            "callback_id": callback_id,
            "action_ts": _ts(),
            "message_ts": (message or {}).get("ts", "1.0"),
            "message": message or {"type": "message", "text": "", "user": user_id, "ts": "1.0"},
            "channel": {"id": channel_id, "name": "general"},
            "response_url": response_url,
        }
    )
    return body


def view_submission(
    callback_id: str,
    values: Optional[Dict[str, Dict[str, Any]]] = None,
    *,
    private_metadata: str = "",
    view_id: str = "V0000000000",
    user_id: str = DEFAULT_USER_ID,
    team_id: str = DEFAULT_TEAM_ID,
    api_app_id: str = DEFAULT_APP_ID,
    response_urls: Optional[List[Dict[str, Any]]] = None,
    trigger_id: str = "111.222.test",
) -> Dict[str, Any]:
    """A `view_submission` payload for a modal.

    `values` uses the same shape as `view["state"]["values"]`, e.g.
    `{"block_id": {"action_id": {"type": "plain_text_input", "value": "hi"}}}`.
    """
    body = _interactive_base(
        "view_submission", user_id=user_id, team_id=team_id, api_app_id=api_app_id, trigger_id=trigger_id
    )
    body.update(
        {
            "view": {
                "id": view_id,
                "team_id": team_id,
                "type": "modal",
                "callback_id": callback_id,
                "private_metadata": private_metadata,
                "state": {"values": values or {}},
                "hash": "1.test",
                "app_id": api_app_id,
                "bot_id": "B0000000000",
            },
            "response_urls": response_urls or [],
        }
    )
    return body


def to_http_body(payload: Dict[str, Any]) -> str:
    """Encodes a payload the way Slack sends it over HTTP.

    Events API payloads are sent as JSON, slash commands as form fields, and interactivity
    payloads as a form with a single `payload` field.
    """
    if "command" in payload and "type" not in payload:
        return urlencode(payload)
    if payload.get("type") in ("event_callback", "url_verification", "app_rate_limited"):
        return json.dumps(payload)
    return urlencode({"payload": json.dumps(payload)})


def signed_headers(body: str, signing_secret: str, timestamp: Optional[int] = None) -> Dict[str, str]:
    """The headers of a request signed with the given signing secret."""
    ts = str(timestamp if timestamp is not None else int(time.time()))
    signature = SignatureVerifier(signing_secret).generate_signature(timestamp=ts, body=body)
    content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
    return {
        "content-type": content_type,
        "x-slack-request-timestamp": ts,
        "x-slack-signature": signature or "",
    }
