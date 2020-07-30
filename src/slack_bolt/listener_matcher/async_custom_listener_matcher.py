import inspect
from typing import Callable, Awaitable

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from .async_listener_matcher import AsyncListenerMatcher
from ..logger import get_bolt_app_logger


class AsyncCustomListenerMatcher(AsyncListenerMatcher):

    def __init__(
        self,
        *,
        app_name: str,
        func: Callable[..., Awaitable[bool]]
    ):
        self.app_name = app_name
        self.func = func
        self.arg_names = inspect.getfullargspec(func).args
        self.logger = get_bolt_app_logger(self.app_name, self.func)

    async def async_matches(self, req: AsyncBoltRequest, resp: BoltResponse) -> bool:
        return await self.func(**build_required_kwargs(
            logger=self.logger,
            required_arg_names=self.arg_names,
            req=req,
            resp=resp
        ))
