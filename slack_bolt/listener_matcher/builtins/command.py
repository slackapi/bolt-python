# pytype: skip-file
from logging import Logger

from slack_bolt.request.payload_utils import is_slash_command

from typing import Any, Optional, Union, Dict

from ..listener_matcher import ListenerMatcher

from .builtin_listener_matcher import build_listener_matcher
from .utils import _matches, Pattern


def command(
    command: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    def func(body: Dict[str, Any]) -> bool:
        return is_slash_command(body) and _matches(command, body["command"])

    return build_listener_matcher(func, asyncio, base_logger)
