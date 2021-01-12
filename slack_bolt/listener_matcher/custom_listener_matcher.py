import inspect
from logging import Logger
from typing import Callable, Sequence

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.logger import get_bolt_app_logger
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .listener_matcher import ListenerMatcher


class CustomListenerMatcher(ListenerMatcher):
    app_name: str
    func: Callable[..., bool]
    arg_names: Sequence[str]
    logger: Logger

    def __init__(self, *, app_name: str, func: Callable[..., bool]):
        self.app_name = app_name
        self.func = func
        self.arg_names = inspect.getfullargspec(func).args
        self.logger = get_bolt_app_logger(self.app_name, self.func)

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
