"""Bolt specific error types."""

from typing import Optional, Union


class BoltError(Exception):
    """General class in a Bolt app"""


class BoltUnhandledRequestError(BoltError):
    request: "BoltRequest"  # type: ignore[name-defined]
    body: dict
    current_response: Optional["BoltResponse"]  # type: ignore[name-defined]
    last_global_middleware_name: Optional[str]

    def __init__(
        self,
        *,
        request: Union["BoltRequest", "AsyncBoltRequest"],  # type: ignore[name-defined]
        current_response: Optional["BoltResponse"],  # type: ignore[name-defined]
        last_global_middleware_name: Optional[str] = None,
    ):
        self.request = request
        self.body = request.body if request is not None else {}
        self.current_response = current_response
        self.last_global_middleware_name = last_global_middleware_name

    def __str__(self) -> str:
        return "unhandled request error"
