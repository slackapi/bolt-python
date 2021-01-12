from abc import abstractmethod, ABCMeta
from typing import Callable, Awaitable, Tuple, Optional, Sequence

from slack_bolt.listener_matcher.async_listener_matcher import AsyncListenerMatcher
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from ..kwargs_injection.async_utils import build_async_required_kwargs


class AsyncListener(metaclass=ABCMeta):
    matchers: Sequence[AsyncListenerMatcher]
    middleware: Sequence[AsyncMiddleware]
    ack_function: Callable[..., Awaitable[BoltResponse]]
    lazy_functions: Sequence[Callable[..., Awaitable[None]]]
    auto_acknowledgement: bool

    async def async_matches(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
    ) -> bool:
        is_matched: bool = False
        for matcher in self.matchers:
            is_matched = await matcher.async_matches(req, resp)
            if not is_matched:
                return is_matched
        return is_matched

    async def run_async_middleware(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
    ) -> Tuple[Optional[BoltResponse], bool]:
        """Runs an async middleware.

        :param req: The incoming request
        :param resp: Thee current response
        :return: A tuple of the processed response and a flag indicating termination
        """
        for m in self.middleware:
            middleware_state = {"next_called": False}

            async def _next():
                middleware_state["next_called"] = True

            resp = await m.async_process(req=req, resp=resp, next=_next)
            if not middleware_state["next_called"]:
                # next() was not called in this middleware
                return (resp, True)
        return (resp, False)

    @abstractmethod
    async def run_ack_function(
        self, *, request: AsyncBoltRequest, response: BoltResponse
    ) -> BoltResponse:
        """Runs all the registered middleware and then run the listener function.

        :param request: The incoming request
        :param response: The current response
        :return: The processed response
        """
        raise NotImplementedError()


import inspect
from logging import Logger
from typing import Callable, Awaitable

from slack_bolt.listener_matcher.async_listener_matcher import AsyncListenerMatcher
from slack_bolt.logger import get_bolt_app_logger
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncCustomListener(AsyncListener):
    app_name: str
    ack_function: Callable[..., Awaitable[Optional[BoltResponse]]]
    lazy_functions: Sequence[Callable[..., Awaitable[None]]]
    matchers: Sequence[AsyncListenerMatcher]
    middleware: Sequence[AsyncMiddleware]
    auto_acknowledgement: bool
    arg_names: Sequence[str]
    logger: Logger

    def __init__(
        self,
        *,
        app_name: str,
        ack_function: Callable[..., Awaitable[Optional[BoltResponse]]],
        lazy_functions: Sequence[Callable[..., Awaitable[None]]],
        matchers: Sequence[AsyncListenerMatcher],
        middleware: Sequence[AsyncMiddleware],
        auto_acknowledgement: bool = False,
    ):
        self.app_name = app_name
        self.ack_function = ack_function
        self.lazy_functions = lazy_functions
        self.matchers = matchers
        self.middleware = middleware
        self.auto_acknowledgement = auto_acknowledgement
        self.arg_names = inspect.getfullargspec(ack_function).args
        self.logger = get_bolt_app_logger(app_name, self.ack_function)

    async def run_ack_function(
        self,
        *,
        request: AsyncBoltRequest,
        response: BoltResponse,
    ) -> Optional[BoltResponse]:
        return await self.ack_function(
            **build_async_required_kwargs(
                logger=self.logger,
                required_arg_names=self.arg_names,
                request=request,
                response=response,
                this_func=self.ack_function,
            )
        )


builtin_async_listener_classes = [
    AsyncCustomListener,
]
for cls in builtin_async_listener_classes:
    AsyncListener.register(cls)
