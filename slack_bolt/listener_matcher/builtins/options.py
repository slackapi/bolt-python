# pytype: skip-file
from logging import Logger

from slack_bolt.error import BoltError
from slack_bolt.request.payload_utils import (
    is_block_suggestion,
    is_dialog_suggestion,
)

from typing import Any, Optional, Union, Dict

from ..listener_matcher import ListenerMatcher

from .builtin_listener_matcher import build_listener_matcher
from .utils import _matches, Pattern


def options(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):

        def func(body: Dict[str, Any]) -> bool:
            return _block_suggestion(constraints, body) or _dialog_suggestion(constraints, body)

        return build_listener_matcher(func, asyncio, base_logger)

    if "action_id" in constraints:
        return block_suggestion(constraints["action_id"], asyncio)
    if "callback_id" in constraints:
        return dialog_suggestion(constraints["callback_id"], asyncio)
    else:
        raise BoltError(f"options ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def _block_suggestion(
    action_id: Union[str, Pattern],
    body: Dict[str, Any],
) -> bool:
    return is_block_suggestion(body) and _matches(action_id, body["action_id"])


def block_suggestion(
    action_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return _block_suggestion(action_id, body)

    return build_listener_matcher(func, asyncio, base_logger)


def _dialog_suggestion(
    callback_id: Union[str, Pattern],
    body: Dict[str, Any],
) -> bool:
    return is_dialog_suggestion(body) and _matches(callback_id, body["callback_id"])


def dialog_suggestion(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return _dialog_suggestion(callback_id, body)

    return build_listener_matcher(func, asyncio, base_logger)
