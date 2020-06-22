import inspect
import sys
if sys.version_info.major == 3 and sys.version_info.minor <= 6:
    from re import _pattern_type as Pattern
else:
    from re import Pattern
from typing import Callable
from typing import Union, Optional, Dict

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .listener_matcher import ListenerMatcher
from ..logger import get_bolt_logger


class BuiltinListenerMatcher(ListenerMatcher):

    def __init__(
        self,
        *,
        func: Callable[..., bool]
    ):
        self.func = func
        self.arg_names = inspect.getfullargspec(func).args
        self.logger = get_bolt_logger(self.func)

    def matches(self, req: BoltRequest, resp: BoltResponse) -> bool:
        return self.func(**build_required_kwargs(
            logger=self.logger,
            required_arg_names=self.arg_names,
            req=req,
            resp=resp
        ))


# -------------
# events


def event(constraints: Union[str, Pattern, Dict[str, str]]) -> ListenerMatcher:
    if isinstance(constraints, (str, Pattern)):
        event_type: Union[str, Pattern] = constraints

        def func(payload: dict) -> bool:
            return _is_valid_event_payload(payload) \
                   and _matches(event_type, payload["event"]["type"])

        return BuiltinListenerMatcher(func=func)

    elif "type" in constraints:
        def func(payload: dict) -> bool:
            if _is_valid_event_payload(payload):
                event = payload["event"]
                expected_type = constraints["type"]
                expected_subtype = constraints["subtype"] if "subtype" in constraints else None
                if expected_subtype:
                    return "subtype" in event \
                           and _matches(expected_type, event["type"]) \
                           and _matches(expected_subtype, event["subtype"])
                else:
                    return _matches(expected_type, event["type"])
            else:
                return False

        return BuiltinListenerMatcher(func=func)

    raise ValueError(f"event ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


# -------------
# slash commands

def command(command: Union[str, Pattern]) -> ListenerMatcher:
    def func(payload: dict) -> bool:
        return payload \
               and "command" in payload \
               and _matches(command, payload["command"])

    return BuiltinListenerMatcher(func=func)


# -------------
# shortcuts

def shortcut(constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]]) -> ListenerMatcher:
    if isinstance(constraints, (str, Pattern)):
        callback_id: Union[str, Pattern] = constraints

        def func(payload: dict) -> bool:
            return payload \
                   and "callback_id" in payload \
                   and _matches(callback_id, payload["callback_id"])

        return BuiltinListenerMatcher(func=func)

    elif "type" in constraints and "callback_id" in constraints:
        if constraints["type"] == "shortcut":
            return global_shortcut(constraints["callback_id"])
        elif constraints["type"] == "message_action":
            return message_shortcut(constraints["callback_id"])

    raise ValueError(f"shortcut ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def global_shortcut(callback_id: Union[str, Pattern]) -> ListenerMatcher:
    def func(payload: dict) -> bool:
        return payload \
               and _is_expected_type(payload, "shortcut") \
               and "callback_id" in payload \
               and _matches(callback_id, payload["callback_id"])

    return BuiltinListenerMatcher(func=func)


def message_shortcut(callback_id: Union[str, Pattern]) -> ListenerMatcher:
    def func(payload: dict) -> bool:
        return payload \
               and _is_expected_type(payload, "message_action") \
               and "callback_id" in payload \
               and _matches(callback_id, payload["callback_id"])

    return BuiltinListenerMatcher(func=func)


# -------------
# action

def action(constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]]) -> ListenerMatcher:
    if isinstance(constraints, (str, Pattern)):
        return block_action(constraints)
    elif "type" in constraints:
        if constraints["type"] == "block_actions":
            return block_action(constraints["action_id"])

    raise ValueError(f"action ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def block_action(action_id: Union[str, Pattern]) -> ListenerMatcher:
    def func(payload: dict) -> bool:
        return payload \
               and _is_expected_type(payload, "block_actions") \
               and "actions" in payload \
               and _matches(action_id, payload["actions"][0]["action_id"])

    return BuiltinListenerMatcher(func=func)


# -------------------------
# view

def view(constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]]) -> ListenerMatcher:
    if isinstance(constraints, (str, Pattern)):
        return view_submission(constraints)
    elif "type" in constraints:
        if constraints["type"] == "view_submission":
            return view_submission(constraints["callback_id"])

    raise ValueError(f"view ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def view_submission(callback_id: Union[str, Pattern]) -> ListenerMatcher:
    def func(payload: dict) -> bool:
        return payload \
               and _is_expected_type(payload, "view_submission") \
               and "view" in payload \
               and "callback_id" in payload["view"] \
               and _matches(callback_id, payload["view"]["callback_id"])

    return BuiltinListenerMatcher(func=func)


# -------------
# options

def options(constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]]) -> ListenerMatcher:
    if isinstance(constraints, (str, Pattern)):
        return block_suggestion(constraints)
    elif "action_id" in constraints:
        return block_suggestion(constraints["action_id"])
    elif "callback_id" in constraints:
        return dialog_suggestion(constraints["callback_id"])
    else:
        raise ValueError(f"options ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def block_suggestion(action_id: Union[str, Pattern]) -> ListenerMatcher:
    def func(payload: dict) -> bool:
        return payload \
               and _is_expected_type(payload, "block_suggestion") \
               and "action_id" in payload \
               and _matches(action_id, payload["action_id"])

    return BuiltinListenerMatcher(func=func)


def dialog_suggestion(callback_id: Union[str, Pattern]) -> ListenerMatcher:
    def func(payload: dict) -> bool:
        return payload \
               and _is_expected_type(payload, "dialog_suggestion") \
               and "callback_id" in payload \
               and _matches(callback_id, payload["callback_id"])

    return BuiltinListenerMatcher(func=func)


# -------------------------

def _is_valid_event_payload(payload: dict) -> bool:
    return payload \
           and _is_expected_type(payload, "event_callback") \
           and "event" in payload \
           and "type" in payload["event"]


def _is_expected_type(payload: dict, expected: str) -> bool:
    return payload \
           and "type" in payload \
           and payload["type"] == expected


def _matches(str_or_pattern: Union[str, Pattern], input: Optional[str]) -> bool:
    if str is None:
        return False

    if isinstance(str_or_pattern, str):
        exact_match_str: str = str_or_pattern
        return input == exact_match_str
    elif isinstance(str_or_pattern, Pattern):
        pattern: Pattern = str_or_pattern
        return pattern.search(input)
    else:
        raise ValueError(f"{str_or_pattern} ({type(str_or_pattern)}) must be either str or Pattern")
