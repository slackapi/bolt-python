# pytype: skip-file
from logging import Logger

from slack_bolt.error import BoltError
from slack_bolt.request.payload_utils import (
    is_global_shortcut,
    is_message_shortcut,
    is_shortcut,
)

from typing import Any, Optional, Union, Dict

from ..listener_matcher import ListenerMatcher

from .builtin_listener_matcher import build_listener_matcher
from .utils import _matches, Pattern


def shortcut(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):
        callback_id: Union[str, Pattern] = constraints

        def func(body: Dict[str, Any]) -> bool:
            return is_shortcut(body) and _matches(callback_id, body["callback_id"])

        return build_listener_matcher(func, asyncio, base_logger)

    elif "type" in constraints and "callback_id" in constraints:
        if constraints["type"] == "shortcut":
            return global_shortcut(constraints["callback_id"], asyncio)
        if constraints["type"] == "message_action":
            return message_shortcut(constraints["callback_id"], asyncio)

    raise BoltError(f"shortcut ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def global_shortcut(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return is_global_shortcut(body) and _matches(callback_id, body["callback_id"])

    return build_listener_matcher(func, asyncio, base_logger)


def message_shortcut(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return is_message_shortcut(body) and _matches(callback_id, body["callback_id"])

    return build_listener_matcher(func, asyncio, base_logger)
