# pytype: skip-file
from logging import Logger

from slack_bolt.error import BoltError
from .action import is_block_id_match
from slack_bolt.request.payload_utils import (
    is_block_actions,
    is_function_interactivity,
)

from typing import Any, Optional, Union, Dict

from ..listener_matcher import ListenerMatcher

from .builtin_listener_matcher import build_listener_matcher
from .utils import _matches, Pattern


def function_action(
    callback_id: Union[str, Pattern],
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):

        def func(body: Dict[str, Any]) -> bool:
            return (
                _function_block_action(callback_id, constraints, body)
            )

        return build_listener_matcher(func, asyncio, base_logger)

    elif "type" in constraints:
        action_type = constraints["type"]
        if action_type == "block_actions":
            return function_block_action(callback_id, constraints, asyncio)

        raise BoltError(f"type: {action_type} is unsupported")
    elif "action_id" in constraints:
        # The default value is "block_actions"
        return function_block_action(callback_id, constraints, asyncio)

    raise BoltError(f"action ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def _function_block_action(
    callback_id: Union[str, Pattern],
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    body: Dict[str, Any],
) -> bool:
    if (is_function_interactivity(body) is False
            and is_block_actions(body) is False):
        return False

    if _matches(callback_id, body.get("function_data", {}).get("function", {}).get("callback_id", "")) is False:
        return False

    return is_block_id_match(constraints, body)


def function_block_action(
    callback_id: Union[str, Pattern],
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return _function_block_action(callback_id, constraints, body)

    return build_listener_matcher(func, asyncio, base_logger)
