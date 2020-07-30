import inspect
from logging import Logger
from typing import Callable, List, Awaitable

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.listener_matcher.async_listener_matcher import AsyncListenerMatcher
from slack_bolt.logger import get_bolt_app_logger
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from .async_listener import AsyncListener


class AsyncCustomListener(AsyncListener):
    app_name: str
    func: Callable[..., Awaitable[BoltResponse]]
    matchers: List[AsyncListenerMatcher]
    middleware: List[AsyncMiddleware]
    auto_acknowledgement: bool
    arg_names: List[str]
    logger: Logger

    def __init__(
        self,
        *,
        app_name: str,
        func: Callable[..., Awaitable[BoltResponse]],
        matchers: List[AsyncListenerMatcher],
        middleware: List[AsyncMiddleware],
        auto_acknowledgement: bool = False,
    ):
        self.app_name = app_name
        self.func = func
        self.matchers = matchers
        self.middleware = middleware
        self.auto_acknowledgement = auto_acknowledgement
        self.arg_names = inspect.getfullargspec(func).args
        self.logger = get_bolt_app_logger(app_name, self.func)

    async def __call__(
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
    ) -> BoltResponse:
        return await self.func(**build_required_kwargs(
            logger=self.logger,
            required_arg_names=self.arg_names,
            req=req,
            resp=resp
        ))
