import inspect
from abc import ABCMeta, abstractmethod
from logging import Logger
from typing import Callable, Dict, Any, Awaitable, Optional

from slack_bolt.listener.async_internals import (
    _build_all_available_args,
)
from slack_bolt.listener.internals import (
    _convert_all_available_args_to_kwargs,
)

from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse


class AsyncListenerCompletionHandler(metaclass=ABCMeta):
    @abstractmethod
    async def handle(
        self,
        request: AsyncBoltRequest,
        response: Optional[BoltResponse],
    ) -> None:
        """Handles an unhandled exception.

        Args:
            error: The raised exception.
            request: The request.
            response: The response.
        """
        raise NotImplementedError()


class AsyncCustomListenerCompletionHandler(AsyncListenerCompletionHandler):
    def __init__(self, logger: Logger, func: Callable[..., Awaitable[None]]):
        self.func = func
        self.logger = logger
        self.arg_names = inspect.getfullargspec(func).args

    async def handle(
        self,
        request: AsyncBoltRequest,
        response: Optional[BoltResponse],
    ) -> None:
        all_available_args = _build_all_available_args(
            logger=self.logger,
            request=request,
            response=response,
        )
        kwargs: Dict[str, Any] = _convert_all_available_args_to_kwargs(
            all_available_args=all_available_args,
            arg_names=self.arg_names,
            logger=self.logger,
        )
        await self.func(**kwargs)


class AsyncDefaultListenerCompletionHandler(AsyncListenerCompletionHandler):
    def __init__(self, logger: Logger):
        self.logger = logger

    async def handle(
        self,
        request: AsyncBoltRequest,
        response: Optional[BoltResponse],
    ):
        pass
