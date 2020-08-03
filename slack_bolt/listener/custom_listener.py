import inspect
from logging import Logger
from typing import Callable, List

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.listener_matcher import ListenerMatcher
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from .listener import Listener
from ..logger import get_bolt_app_logger
from ..middleware import Middleware


class CustomListener(Listener):
    app_name: str
    func: Callable[..., BoltResponse]
    matchers: List[ListenerMatcher]
    middleware: List[Middleware]
    auto_acknowledgement: bool
    arg_names: List[str]
    logger: Logger

    def __init__(
        self,
        *,
        app_name: str,
        func: Callable[..., BoltResponse],
        matchers: List[ListenerMatcher],
        middleware: List[Middleware],
        auto_acknowledgement: bool = False,
    ):
        self.app_name = app_name
        self.func = func
        self.matchers = matchers
        self.middleware = middleware
        self.auto_acknowledgement = auto_acknowledgement
        self.arg_names = inspect.getfullargspec(func).args
        self.logger = get_bolt_app_logger(app_name, self.func)

    def run_ack_function(
        self, *, request: BoltRequest, response: BoltResponse,
    ) -> BoltResponse:
        return self.func(
            **build_required_kwargs(
                logger=self.logger,
                required_arg_names=self.arg_names,
                request=request,
                response=response,
            )
        )
