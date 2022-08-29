from typing import List, Union, Pattern, Callable, Dict, Optional, Sequence
from logging import Logger

from slack_bolt.listener_matcher import builtins as builtin_matchers

from slack_bolt.response import BoltResponse
from slack_bolt.middleware import Middleware


# TDOD this is a duplicate function in App
def _to_listener_functions(
    kwargs: dict,
) -> Optional[Sequence[Callable[..., Optional[BoltResponse]]]]:
    if kwargs:
        functions = [kwargs["ack"]]
        for sub in kwargs["lazy"]:
            functions.append(sub)
        return functions
    return None


class Function:

    function: Optional[Callable[..., Optional[BoltResponse]]] = None

    def __init__(
        self,
        register_listener: Callable[..., Optional[Callable[..., Optional[BoltResponse]]]],
        base_logger: Logger,
        callback_id: Union[str, Pattern],
    ):
        self._register_listener = register_listener
        self._base_logger = base_logger
        self.callback_id = callback_id

    def register_listener(
        self,
        functions: List[Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        primary_matcher = builtin_matchers.function_event(callback_id=self.callback_id, base_logger=self._base_logger)
        self.function = self._register_listener(functions, primary_matcher, matchers, middleware, True)
        return self

    def __call__(self, *args, **kwargs) -> Optional[Callable[..., Optional[BoltResponse]]]:
        if self.function is not None:
            return self.function(*args, **kwargs)
        return None

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        """Registers a new action listener. This method can be used as either a decorator or a method."""

        def __call__(*args, **kwargs):
            functions = _to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.function_action(self.callback_id, constraints, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    @property
    def __isabstractmethod__(self):
        return getattr(self.function, "__isabstractmethod__", False)
