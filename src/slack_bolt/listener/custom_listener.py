import inspect
from typing import Callable, List

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.listener_matcher import ListenerMatcher
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .listener import Listener
from ..logger import get_bolt_app_logger


class CustomListener(Listener):

    def __init__(
        self,
        *,
        app_name: str,
        func: Callable[[any], BoltResponse],
        matchers: List[ListenerMatcher],
    ):
        self.app_name = app_name
        self.func = func
        self.matchers = matchers
        self.arg_names = inspect.getfullargspec(func).args
        self.logger = get_bolt_app_logger(app_name, self.func)

    def __call__(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse) -> BoltResponse:
        return self.func(**build_required_kwargs(
            logger=self.logger,
            required_arg_names=self.arg_names,
            req=req,
            resp=resp
        ))
