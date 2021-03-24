from abc import ABCMeta, abstractmethod
from typing import Callable, Optional

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class Middleware(metaclass=ABCMeta):
    """A middleware can process request data before other middleware and listener functions."""

    @abstractmethod
    def process(
        self,
        *,
        req: BoltRequest,
        resp: BoltResponse,
        next: Callable[[], BoltResponse],
    ) -> Optional[BoltResponse]:
        """Processes a request data before other middleware and listeners.
        A middleware calls `next()` function if the chain should continue.

            @app.middleware
            def simple_middleware(req, resp, next):
                # do something here
                next()

        Args:
            req: The incoming request
            resp: The response
            next: The function to tell the chain that it can continue

        Returns:
            Processed response (optional)
        """
        raise NotImplementedError()

    @property
    def name(self) -> str:
        """The name of this middleware"""
        return f"{self.__module__}.{self.__class__.__name__}"
