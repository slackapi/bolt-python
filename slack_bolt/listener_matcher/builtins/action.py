# pytype: skip-file
from logging import Logger

from slack_bolt.error import BoltError
from slack_bolt.request.payload_utils import (
    is_block_actions,
    is_attachment_action,
    is_dialog_submission,
    is_dialog_cancellation,
    is_workflow_step_edit,
    to_action,
)

from typing import Any, Optional, Union, Dict

from ..listener_matcher import ListenerMatcher

from .builtin_listener_matcher import build_listener_matcher
from .utils import _matches, Pattern


# -------------
# action


def action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):

        def func(body: Dict[str, Any]) -> bool:
            return (
                _block_action(constraints, body)
                or _attachment_action(constraints, body)
                or _dialog_submission(constraints, body)
                or _dialog_cancellation(constraints, body)
                or _workflow_step_edit(constraints, body)
            )

        return build_listener_matcher(func, asyncio, base_logger)

    elif "type" in constraints:
        action_type = constraints["type"]
        if action_type == "block_actions":
            return block_action(constraints, asyncio)
        if action_type == "interactive_message":
            return attachment_action(constraints["callback_id"], asyncio)
        if action_type == "dialog_submission":
            return dialog_submission(constraints["callback_id"], asyncio)
        if action_type == "dialog_cancellation":
            return dialog_cancellation(constraints["callback_id"], asyncio)
        # https://api.slack.com/workflows/steps
        if action_type == "workflow_step_edit":
            return workflow_step_edit(constraints["callback_id"], asyncio)

        raise BoltError(f"type: {action_type} is unsupported")
    elif "action_id" in constraints:
        # The default value is "block_actions"
        return block_action(constraints, asyncio)

    raise BoltError(f"action ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def _block_action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    body: Dict[str, Any],
) -> bool:
    if is_block_actions(body) is False:
        return False

    return is_block_id_match(constraints, body)


def is_block_id_match(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    body: Dict[str, Any]
) -> bool:
    action = to_action(body)
    if isinstance(constraints, (str, Pattern)):
        action_id = constraints
        return _matches(action_id, action["action_id"])
    elif isinstance(constraints, dict):
        # block_id matching is optional
        block_id: Optional[Union[str, Pattern]] = constraints.get("block_id")
        block_id_matched = block_id is None or _matches(block_id, action.get("block_id"))
        action_id_matched = _matches(constraints["action_id"], action["action_id"])
        return block_id_matched and action_id_matched


def block_action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return _block_action(constraints, body)

    return build_listener_matcher(func, asyncio, base_logger)


def _attachment_action(
    callback_id: Union[str, Pattern],
    body: Dict[str, Any],
) -> bool:
    return is_attachment_action(body) and _matches(callback_id, body["callback_id"])


def attachment_action(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return _attachment_action(callback_id, body)

    return build_listener_matcher(func, asyncio, base_logger)


def _dialog_submission(
    callback_id: Union[str, Pattern],
    body: Dict[str, Any],
) -> bool:
    return is_dialog_submission(body) and _matches(callback_id, body["callback_id"])


def dialog_submission(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return _dialog_submission(callback_id, body)

    return build_listener_matcher(func, asyncio, base_logger)


def _dialog_cancellation(
    callback_id: Union[str, Pattern],
    body: Dict[str, Any],
) -> bool:
    return is_dialog_cancellation(body) and _matches(callback_id, body["callback_id"])


def dialog_cancellation(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return _dialog_cancellation(callback_id, body)

    return build_listener_matcher(func, asyncio, base_logger)


def _workflow_step_edit(
    callback_id: Union[str, Pattern],
    body: Dict[str, Any],
) -> bool:
    return is_workflow_step_edit(body) and _matches(callback_id, body["callback_id"])


def workflow_step_edit(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return _workflow_step_edit(callback_id, body)

    return build_listener_matcher(func, asyncio, base_logger)
