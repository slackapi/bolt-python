# pytype: skip-file
from logging import Logger

from slack_bolt.error import BoltError
from slack_bolt.request.payload_utils import (
    is_view_submission,
    is_view_closed,
    is_workflow_step_save,
)

from typing import Any, Optional, Union, Dict

from ..listener_matcher import ListenerMatcher

from .builtin_listener_matcher import build_listener_matcher
from .utils import _matches, Pattern


def view(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):
        return view_submission(constraints, asyncio)
    elif "type" in constraints:
        if constraints["type"] == "view_submission":
            return view_submission(constraints["callback_id"], asyncio)
        if constraints["type"] == "view_closed":
            return view_closed(constraints["callback_id"], asyncio)

    raise BoltError(f"view ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def view_submission(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return is_view_submission(body) and _matches(callback_id, body["view"]["callback_id"])

    return build_listener_matcher(func, asyncio, base_logger)


def view_closed(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return is_view_closed(body) and _matches(callback_id, body["view"]["callback_id"])

    return build_listener_matcher(func, asyncio, base_logger)


def workflow_step_save(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return is_workflow_step_save(body) and _matches(callback_id, body["view"]["callback_id"])

    return build_listener_matcher(func, asyncio, base_logger)
