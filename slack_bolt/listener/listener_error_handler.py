from abc import ABCMeta, abstractmethod
from logging import Logger
from typing import Callable, Dict, Any, Optional

from slack_bolt.kwargs_injection import build_required_kwargs
from slack_bolt.request.request import BoltRequest
from slack_bolt.response.response import BoltResponse
from slack_bolt.util.utils import get_arg_names_of_callable


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
    def __init__(self, logger: Logger, func: Callable[..., Optional[BoltResponse]]):
        self.func = func
        self.logger = logger
        self.arg_names = get_arg_names_of_callable(func)

    def handle(
        self,
        error: Exception,
        request: BoltRequest,
        response: Optional[BoltResponse],
    ):
        kwargs: Dict[str, Any] = build_required_kwargs(
            required_arg_names=self.arg_names,
            logger=self.logger,
            error=error,
            request=request,
            response=response,
            next_keys_required=False,
        )
        returned_response = self.func(**kwargs)
        if returned_response is not None and isinstance(returned_response, BoltResponse):
            response.status = returned_response.status
            response.headers = returned_response.headers
            response.body = returned_response.body


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
