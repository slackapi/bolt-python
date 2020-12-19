from typing import Dict, Any

from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.request.internals import (
    extract_enterprise_id,
    extract_team_id,
    extract_user_id,
    extract_channel_id,
)


def build_async_context(
    context: AsyncBoltContext,
    payload: Dict[str, Any],
) -> AsyncBoltContext:
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
