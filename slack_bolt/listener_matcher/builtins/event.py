# pytype: skip-file
import re
from logging import Logger

from slack_bolt.error import BoltError
from slack_bolt.request.payload_utils import (
    is_function,
    is_event,
)
from ...logger.messages import error_message_event_type

from typing import Any, Sequence, Optional, Union, Dict

from ..listener_matcher import ListenerMatcher

from .builtin_listener_matcher import build_listener_matcher
from .utils import _matches, Pattern


def event(
    constraints: Union[
        str,
        Pattern,
        Dict[str, Optional[Union[str, Sequence[Optional[Union[str, Pattern]]]]]],
    ],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if isinstance(constraints, (str, Pattern)):
        event_type: Union[str, Pattern] = constraints
        _verify_message_event_type(event_type)

        def func(body: Dict[str, Any]) -> bool:
            return is_event(body) and _matches(event_type, body["event"]["type"])

        return build_listener_matcher(func, asyncio, base_logger)

    elif "type" in constraints:
        _verify_message_event_type(constraints["type"])

        def func(body: Dict[str, Any]) -> bool:
            if is_event(body):
                return _check_event_subtype(
                    event_payload=body["event"],
                    constraints=constraints,
                )
            return False

        return build_listener_matcher(func, asyncio, base_logger)

    raise BoltError(f"event ({constraints}: {type(constraints)}) must be any of str, Pattern, and dict")


def message_event(
    constraints: Dict[str, Optional[Union[str, Sequence[Optional[Union[str, Pattern]]]]]],
    keyword: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if "type" in constraints and keyword is not None:
        _verify_message_event_type(constraints["type"])

        def func(body: Dict[str, Any]) -> bool:
            if is_event(body):
                is_valid_subtype = _check_event_subtype(
                    event_payload=body["event"],
                    constraints=constraints,
                )
                if is_valid_subtype is True:
                    # Check keyword matching
                    text = body.get("event", {}).get("text", "")
                    match_result = re.findall(keyword, text)
                    if match_result is not None and match_result != []:
                        return True
            return False

        return build_listener_matcher(func, asyncio, base_logger)

    raise BoltError(f"event ({constraints}: {type(constraints)}) must be dict")


def _check_event_subtype(event_payload: dict, constraints: dict) -> bool:
    if not _matches(constraints["type"], event_payload["type"]):
        return False
    if "subtype" in constraints:
        expected_subtype: Optional[Union[str, Sequence[Optional[Union[str, Pattern]]]]] = constraints["subtype"]
        if expected_subtype is None:
            # "subtype" in constraints is intentionally None for this pattern
            return "subtype" not in event_payload
        elif isinstance(expected_subtype, (str, Pattern)):
            return "subtype" in event_payload and _matches(expected_subtype, event_payload["subtype"])
        elif isinstance(expected_subtype, Sequence):
            subtypes: Sequence[Optional[Union[str, Pattern]]] = expected_subtype
            for expected in subtypes:
                actual: Optional[str] = event_payload.get("subtype")
                if expected is None:
                    if actual is None:
                        return True
                elif actual is not None and _matches(expected, actual):
                    return True
            return False
        else:
            return "subtype" in event_payload and _matches(expected_subtype, event_payload["subtype"])
    return True


def _verify_message_event_type(event_type: str) -> None:
    if isinstance(event_type, str) and event_type.startswith("message."):
        raise ValueError(error_message_event_type(event_type))
    if isinstance(event_type, Pattern) and "message\\." in event_type.pattern:
        raise ValueError(error_message_event_type(event_type))


def workflow_step_execute(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return (
            is_event(body)
            and _matches("workflow_step_execute", body["event"]["type"])
            and "workflow_step" in body["event"]
            and _matches(callback_id, body["event"]["callback_id"])
        )

    return build_listener_matcher(func, asyncio, base_logger)


def function_event(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return is_function(body) and _matches(callback_id, body.get("event", {}).get("function", {}).get("callback_id", ""))

    return build_listener_matcher(func, asyncio, base_logger)
