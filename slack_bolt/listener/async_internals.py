from logging import Logger
from typing import Dict, Any, Optional

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.request.payload_utils import (
    to_options,
    to_shortcut,
    to_action,
    to_view,
    to_command,
    to_event,
    to_message,
    to_step,
)
from slack_bolt.response import BoltResponse


def _build_all_available_args(
    logger: Logger,
    request: AsyncBoltRequest,
    response: Optional[BoltResponse],
    error: Optional[Exception] = None,
) -> Dict[str, Any]:
    all_available_args = {
        "logger": logger,
        "error": error,
        "client": request.context.client,
        "req": request,
        "request": request,
        "resp": response,
        "response": response,
        "context": request.context,
        # payload
        "body": request.body,
        "options": to_options(request.body),
        "shortcut": to_shortcut(request.body),
        "action": to_action(request.body),
        "view": to_view(request.body),
        "command": to_command(request.body),
        "event": to_event(request.body),
        "message": to_message(request.body),
        "step": to_step(request.body),
        # utilities
        "say": request.context.say,
        "respond": request.context.respond,
    }
    all_available_args["payload"] = (
        all_available_args["options"]
        or all_available_args["shortcut"]
        or all_available_args["action"]
        or all_available_args["view"]
        or all_available_args["command"]
        or all_available_args["event"]
        or all_available_args["message"]
        or all_available_args["step"]
        or request.body
    )
    return all_available_args
