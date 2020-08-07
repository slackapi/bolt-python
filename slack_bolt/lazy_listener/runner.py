from abc import abstractmethod, ABCMeta
from logging import Logger
from typing import Callable

from slack_bolt.lazy_listener.internals import build_runnable_function
from slack_bolt.request import BoltRequest


class LazyListenerRunner(metaclass=ABCMeta):
    logger: Logger

    @abstractmethod
    def start(self, function: Callable[..., None], request: BoltRequest) -> None:
        raise NotImplementedError()

    def run(self, function: Callable[..., None], request: BoltRequest) -> None:
        build_runnable_function(func=function, logger=self.logger, request=request,)()
