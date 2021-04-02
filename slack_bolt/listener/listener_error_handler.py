import inspect
from abc import ABCMeta, abstractmethod
from logging import Logger
from typing import Callable, Dict, Any, Optional

from slack_bolt.listener.internals import (
    _build_all_available_args,
    _convert_all_available_args_to_kwargs,
)

from slack_bolt.request.request import BoltRequest
from slack_bolt.response.response import BoltResponse


class ListenerErrorHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(
        self,
        error: Exception,
        request: BoltRequest,
        response: Optional[BoltResponse],
    ) -> None:
        """Handles an unhandled exception.

        Args:
            error: The raised exception.
            request: The request.
            response: The response.
        """
        raise NotImplementedError()


class CustomListenerErrorHandler(ListenerErrorHandler):
    def __init__(self, logger: Logger, func: Callable[..., None]):
        self.func = func
        self.logger = logger
        self.arg_names = inspect.getfullargspec(func).args

    def handle(
        self,
        error: Exception,
        request: BoltRequest,
        response: Optional[BoltResponse],
    ):
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
        self.func(**kwargs)


class DefaultListenerErrorHandler(ListenerErrorHandler):
    def __init__(self, logger: Logger):
        self.logger = logger

    def handle(
        self,
        error: Exception,
        request: BoltRequest,
        response: Optional[BoltResponse],
    ):
        message = f"Failed to run listener function (error: {error})"
        self.logger.exception(message)
