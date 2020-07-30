import logging
from typing import Set, Callable, Dict, Union

from slack_bolt.request import BoltRequest
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from .args import Args


def build_required_kwargs(
    *,
    logger: logging.Logger,
    required_arg_names: Set[str],
    req: Union[BoltRequest, AsyncBoltRequest],
    resp: BoltResponse,
    next_func: Callable[[], None] = None,
) -> Dict[str, any]:
    all_available_args = {
        "logger": logger,
        "client": req.context.client,
        "req": req,
        "request": req,
        "resp": resp,
        "response": resp,
        "context": req.context,
        "payload": req.payload,
        "body": req.payload,
        "ack": req.context.ack,
        "say": req.context.say,
        "respond": req.context.respond,
        "next": next_func,
    }
    kwargs: Dict[str, any] = {
        k: v
        for k, v in all_available_args.items()
        if k in required_arg_names
    }
    found_arg_names = kwargs.keys()
    for name in required_arg_names:
        if name == "args":
            kwargs[name] = Args(**all_available_args)
        if name not in found_arg_names:
            logger.warning(f"{name} is not a valid argument")
            kwargs[name] = None
    return kwargs
