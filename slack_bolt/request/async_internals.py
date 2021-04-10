from typing import Dict, Any

from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.request.internals import (
    extract_enterprise_id,
    extract_team_id,
    extract_user_id,
    extract_channel_id,
    debug_multiple_response_urls_detected,
)


def build_async_context(
    context: AsyncBoltContext,
    body: Dict[str, Any],
) -> AsyncBoltContext:
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
