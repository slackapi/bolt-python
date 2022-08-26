from typing import List, Union, Pattern, Callable, Dict, Optional, Sequence, Any
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

    def __init__(
        self,
        _register_listener: Callable[..., Optional[Callable[..., Optional[BoltResponse]]]],
        _base_logger: Logger,
        functions: List[Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]],
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
    ):
        self._register_listener = _register_listener
        self._base_logger = _base_logger
        self.callback_id = callback_id

        primary_matcher = builtin_matchers.function_event(callback_id=self.callback_id, base_logger=_base_logger)
        self.function = self._register_listener(functions, primary_matcher, matchers, middleware, True)

    def __call__(self, *args, **kwargs) -> Optional[Callable[..., Optional[BoltResponse]]]:
        return self.function(*args, **kwargs)

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        """Registers a new action listener. This method can be used as either a decorator or a method.

        """

        def __call__(*args, **kwargs):
            print("action reistered")

        return __call__

    @property
    def __isabstractmethod__(self):
        return getattr(self.function, '__isabstractmethod__', False)
