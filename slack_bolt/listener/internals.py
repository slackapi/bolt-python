from logging import Logger
from typing import Optional, Dict, Any, List

from slack_bolt.request.request import BoltRequest
from slack_bolt.response.response import BoltResponse

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


def _build_all_available_args(
    logger: Logger,
    request: BoltRequest,
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


def _convert_all_available_args_to_kwargs(
    all_available_args: Dict[str, Any],
    arg_names: List[str],
    logger: Logger,
) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {  # type: ignore
        k: v for k, v in all_available_args.items() if k in arg_names  # type: ignore
    }
    found_arg_names = kwargs.keys()
    for name in arg_names:
        if name not in found_arg_names:
            logger.warning(f"{name} is not a valid argument")
            kwargs[name] = None
    return kwargs
