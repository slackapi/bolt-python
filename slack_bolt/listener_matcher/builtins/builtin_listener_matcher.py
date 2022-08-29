# pytype: skip-file
from logging import Logger

from ...util.utils import get_arg_names_of_callable

from typing import Callable, Awaitable, Any, Optional, Union, Dict

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from ..listener_matcher import ListenerMatcher
from slack_bolt.logger import get_bolt_logger


# a.k.a Union[ListenerMatcher, "AsyncListenerMatcher"]
class BuiltinListenerMatcher(ListenerMatcher):
    def __init__(
        self,
        *,
        func: Callable[..., Union[bool, Awaitable[bool]]],
        base_logger: Optional[Logger] = None,
    ):
        self.func = func
        self.arg_names = get_arg_names_of_callable(func)
        self.logger = get_bolt_logger(self.func, base_logger)

    def matches(self, req: BoltRequest, resp: BoltResponse) -> bool:
        return self.func(
            **build_required_kwargs(
                logger=self.logger,
                required_arg_names=self.arg_names,
                request=req,
                response=resp,
                this_func=self.func,
            )
        )


def build_listener_matcher(
    func: Callable[..., bool],
    asyncio: bool,
    base_logger: Optional[Logger] = None,
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]:
    if asyncio:
        from ..async_builtins import AsyncBuiltinListenerMatcher

        async def async_fun(body: Dict[str, Any]) -> bool:
            return func(body)

        return AsyncBuiltinListenerMatcher(func=async_fun, base_logger=base_logger)
    else:
        return BuiltinListenerMatcher(func=func, base_logger=base_logger)
