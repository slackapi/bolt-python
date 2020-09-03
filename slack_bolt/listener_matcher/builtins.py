# pytype: skip-file
import inspect
import sys

from ..error import BoltError
from ..util.payload_utils import (
    is_block_actions,
    is_global_shortcut,
    is_message_shortcut,
    is_attachment_action,
    is_dialog_submission,
    is_dialog_cancellation,
    is_workflow_step_edit,
    is_slash_command,
    is_event,
    is_view_submission,
    is_view_closed,
    is_block_suggestion,
    is_dialog_suggestion,
    is_shortcut,
    to_action,
)

if sys.version_info.major == 3 and sys.version_info.minor <= 6:
    from re import _pattern_type as Pattern
else:
    from re import Pattern
from typing import Callable, Awaitable, Any
from typing import Union, Optional, Dict

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .listener_matcher import ListenerMatcher
from slack_bolt.logger import get_bolt_logger


# a.k.a Union[ListenerMatcher, "AsyncListenerMatcher"]
class BuiltinListenerMatcher(ListenerMatcher):
    def __init__(self, *, func: Callable[..., Union[bool, Awaitable[bool]]]):
        self.func = func
        self.arg_names = inspect.getfullargspec(func).args
        self.logger = get_bolt_logger(self.func)

    def matches(self, req: BoltRequest, resp: BoltResponse) -> bool:
        return self.func(
            **build_required_kwargs(
                logger=self.logger,
                required_arg_names=self.arg_names,
                request=req,
                response=resp,
            )
        )


def build_listener_matcher(
    func: Callable[..., bool], asyncio: bool,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if asyncio:
        from .async_builtins import AsyncBuiltinListenerMatcher

        async def async_fun(payload: Dict[str, Any]) -> bool:
            return func(payload)

        return AsyncBuiltinListenerMatcher(func=async_fun)
    else:
        return BuiltinListenerMatcher(func=func)


# -------------
# events


def event(
    constraints: Union[str, Pattern, Dict[str, str]], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if constraints == "message":
        # matches message events that don't have subtype in payload
        constraints = {"type": "message", "subtype": None}

    if isinstance(constraints, (str, Pattern)):
        event_type: Union[str, Pattern] = constraints

        def func(payload: Dict[str, Any]) -> bool:
            return is_event(payload) and _matches(event_type, payload["event"]["type"])

        return build_listener_matcher(func, asyncio)

    elif "type" in constraints:

        def func(payload: Dict[str, Any]) -> bool:
            if is_event(payload):
                event = payload["event"]
                if not _matches(constraints["type"], event["type"]):
                    return False
                if "subtype" in constraints:
                    expected_subtype = constraints["subtype"]
                    if expected_subtype is None:
                        # "subtype" in constraints is intentionally None for this pattern
                        return "subtype" not in event
                    else:
                        return "subtype" in event and _matches(
                            expected_subtype, event["subtype"]
                        )
                return True
            return False

        return build_listener_matcher(func, asyncio)

    raise BoltError(
        f"event ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict"
    )


# -------------
# slash commands


def command(
    command: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_slash_command(payload) and _matches(command, payload["command"])

    return build_listener_matcher(func, asyncio)


# -------------
# shortcuts


def shortcut(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):
        callback_id: Union[str, Pattern] = constraints

        def func(payload: Dict[str, Any]) -> bool:
            return is_shortcut(payload) and _matches(
                callback_id, payload["callback_id"]
            )

        return build_listener_matcher(func, asyncio)

    elif "type" in constraints and "callback_id" in constraints:
        if constraints["type"] == "shortcut":
            return global_shortcut(constraints["callback_id"], asyncio)
        if constraints["type"] == "message_action":
            return message_shortcut(constraints["callback_id"], asyncio)

    raise BoltError(
        f"shortcut ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict"
    )


def global_shortcut(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_global_shortcut(payload) and _matches(
            callback_id, payload["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


def message_shortcut(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_message_shortcut(payload) and _matches(
            callback_id, payload["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


# -------------
# action


def action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):
        return block_action(constraints, asyncio)
    elif "type" in constraints:
        action_type = constraints["type"]
        if action_type == "block_actions":
            return block_action(constraints["action_id"], asyncio)
        if action_type == "interactive_message":
            return attachment_action(constraints["callback_id"], asyncio)
        if action_type == "dialog_submission":
            return dialog_submission(constraints["callback_id"], asyncio)
        if action_type == "dialog_cancellation":
            return dialog_cancellation(constraints["callback_id"], asyncio)

        # Still in beta
        # https://api.slack.com/workflows/steps
        if action_type == "workflow_step_edit":
            return workflow_step_edit(constraints["callback_id"], asyncio)

        raise BoltError(f"type: {action_type} is unsupported")

    raise BoltError(
        f"action ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict"
    )


def block_action(
    action_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_block_actions(payload) and _matches(
            action_id, to_action(payload)["action_id"]
        )

    return build_listener_matcher(func, asyncio)


def attachment_action(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_attachment_action(payload) and _matches(
            callback_id, payload["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


def dialog_submission(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_dialog_submission(payload) and _matches(
            callback_id, payload["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


def dialog_cancellation(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_dialog_cancellation(payload) and _matches(
            callback_id, payload["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


def workflow_step_edit(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_workflow_step_edit(payload) and _matches(
            callback_id, payload["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


# -------------------------
# view


def view(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):
        return view_submission(constraints, asyncio)
    elif "type" in constraints:
        if constraints["type"] == "view_submission":
            return view_submission(constraints["callback_id"], asyncio)
        if constraints["type"] == "view_closed":
            return view_closed(constraints["callback_id"], asyncio)

    raise BoltError(
        f"view ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict"
    )


def view_submission(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_view_submission(payload) and _matches(
            callback_id, payload["view"]["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


def view_closed(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_view_closed(payload) and _matches(
            callback_id, payload["view"]["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


# -------------
# options


def options(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):
        return block_suggestion(constraints, asyncio)
    if "action_id" in constraints:
        return block_suggestion(constraints["action_id"], asyncio)
    if "callback_id" in constraints:
        return dialog_suggestion(constraints["callback_id"], asyncio)
    else:
        raise BoltError(
            f"options ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict"
        )


def block_suggestion(
    action_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_block_suggestion(payload) and _matches(
            action_id, payload["action_id"]
        )

    return build_listener_matcher(func, asyncio)


def dialog_suggestion(
    callback_id: Union[str, Pattern], asyncio: bool = False,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(payload: Dict[str, Any]) -> bool:
        return is_dialog_suggestion(payload) and _matches(
            callback_id, payload["callback_id"]
        )

    return build_listener_matcher(func, asyncio)


# -------------------------


def _matches(str_or_pattern: Union[str, Pattern], input: Optional[str]) -> bool:
    if str_or_pattern is None or input is None:
        return False

    if isinstance(str_or_pattern, str):
        exact_match_str: str = str_or_pattern
        return input == exact_match_str
    elif isinstance(str_or_pattern, Pattern):
        pattern: Pattern = str_or_pattern
        return pattern.search(input)
    else:
        raise BoltError(
            f"{str_or_pattern} ({type(str_or_pattern)}) must be either str or Pattern"
        )
