import inspect
from abc import ABCMeta, abstractmethod
from logging import Logger
from typing import Callable, Dict, Any, Optional

from slack_bolt.request.request import BoltRequest
from slack_bolt.response.response import BoltResponse


class ListenerErrorHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(
        self, error: Exception, request: BoltRequest, response: Optional[BoltResponse],
    ) -> None:
        raise NotImplementedError()


class CustomListenerErrorHandler(ListenerErrorHandler):
    def __init__(self, logger: Logger, func: Callable[..., None]):
        self.func = func
        self.logger = logger
        self.arg_names = inspect.getfullargspec(func).args

    def handle(
        self, error: Exception, request: BoltRequest, response: Optional[BoltResponse],
    ):
        all_available_args = {
            "logger": self.logger,
            "error": error,
            "client": request.context.client,
            "req": request,
            "request": request,
            "resp": response,
            "response": response,
            "context": request.context,
            "payload": request.payload,
            "body": request.payload,
            "say": request.context.say,
            "respond": request.context.respond,
        }
        kwargs: Dict[str, Any] = {  # type: ignore
            k: v for k, v in all_available_args.items() if k in self.arg_names  # type: ignore
        }
        found_arg_names = kwargs.keys()
        for name in self.arg_names:
            if name not in found_arg_names:
                self.logger.warning(f"{name} is not a valid argument")
                kwargs[name] = None

        self.func(**kwargs)


class DefaultListenerErrorHandler(ListenerErrorHandler):
    def __init__(self, logger: Logger):
        self.logger = logger

    def handle(
        self, error: Exception, request: BoltRequest, response: Optional[BoltResponse],
    ):
        message = f"Failed to run listener function (error: {error})"
        self.logger.exception(message)
