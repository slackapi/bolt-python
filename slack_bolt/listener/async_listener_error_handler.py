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


class AsyncListenerErrorHandler(metaclass=ABCMeta):
    @abstractmethod
    async def handle(
        self,
        error: Exception,
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


class AsyncCustomListenerErrorHandler(AsyncListenerErrorHandler):
    def __init__(
        self, logger: Logger, func: Callable[..., Awaitable[Optional[BoltResponse]]]
    ):
        self.func = func
        self.logger = logger
        self.arg_names = inspect.getfullargspec(func).args

    async def handle(
        self,
        error: Exception,
        request: AsyncBoltRequest,
        response: Optional[BoltResponse],
    ) -> None:
        all_available_args = _build_all_available_args(
            logger=self.logger,
            error=error,
            request=request,
            response=response,
        )
        kwargs: Dict[str, Any] = _convert_all_available_args_to_kwargs(
            all_available_args=all_available_args,
            arg_names=self.arg_names,
            logger=self.logger,
        )
        returned_response = await self.func(**kwargs)
        if returned_response is not None and isinstance(
            returned_response, BoltResponse
        ):
            response.status = returned_response.status
            response.headers = returned_response.headers
            response.body = returned_response.body


class AsyncDefaultListenerErrorHandler(AsyncListenerErrorHandler):
    def __init__(self, logger: Logger):
        self.logger = logger

    async def handle(
        self,
        error: Exception,
        request: AsyncBoltRequest,
        response: Optional[BoltResponse],
    ):
        message = f"Failed to run listener function (error: {error})"
        self.logger.exception(message)
