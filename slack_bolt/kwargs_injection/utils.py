# pytype: skip-file
import logging
from typing import Callable, Dict, Optional, List, Any

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .args import Args


def build_required_kwargs(
    *,
    logger: logging.Logger,
    required_arg_names: List[str],
    request: BoltRequest,
    response: Optional[BoltResponse],
    next_func: Callable[[], None] = None,
) -> Dict[str, Any]:
    all_available_args = {
        "logger": logger,
        "client": request.context.client,
        "req": request,
        "request": request,
        "resp": response,
        "response": response,
        "context": request.context,
        "payload": request.payload,
        "body": request.payload,
        "ack": request.context.ack,
        "say": request.context.say,
        "respond": request.context.respond,
        "next": next_func,
    }
    kwargs: Dict[str, Any] = {
        k: v for k, v in all_available_args.items() if k in required_arg_names
    }
    found_arg_names = kwargs.keys()
    for name in required_arg_names:
        if name == "args":
            if isinstance(request, BoltRequest):
                kwargs[name] = Args(**all_available_args)
            else:
                logger.warning(
                    f"Unknown Request object type detected ({type(request)})"
                )

        if name not in found_arg_names:
            logger.warning(f"{name} is not a valid argument")
            kwargs[name] = None
    return kwargs
