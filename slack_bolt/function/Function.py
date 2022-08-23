from dataclasses import dataclass
from typing import List, Union, Pattern, Callable, Dict, Optional, Sequence, Any

from slack_bolt.listener_matcher import builtins as builtin_matchers

from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.middleware import Middleware
from slack_bolt.listener_matcher import ListenerMatcher


@dataclass(repr=True, eq=False)
class Listener:
    functions: Sequence[Callable[..., Optional[BoltResponse]]]
    primary_matcher: ListenerMatcher
    matchers: Optional[Sequence[Callable[..., bool]]]
    middleware: Optional[Sequence[Union[Callable, Middleware]]]
    auto_acknowledgement: bool = False,


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


class _Function:
    """Single-dispatch generic method descriptor.
    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
    """

    function_listener: Listener = None
    action_listener: List = []
    view_listener: List = []

    def __init__(
            self,
            func,
            callback_id: Union[str, Pattern],
            matchers: Optional[Sequence[Callable[..., bool]]] = None,
            middleware: Optional[Sequence[Union[Callable, Middleware]]] = None):
        self.callback_id = callback_id
        self.matchers = matchers
        self.middleware = middleware
        self.func = func

    def __call__(
        self,
        *args,
        **kwargs,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        functions = _to_listener_functions(kwargs) if kwargs else list(args)
        primary_matcher = builtin_matchers.function_event(
            callback_id=self.callback_id, base_logger=None)  # TODO logger is None
        self.function_listener = Listener(list(functions), primary_matcher, self.matchers, self.middleware, True)
        return self

    def action(
        self,
        cls,
        method=None,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]] = None,
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        """Registers a new action listener. This method can be used as either a decorator or a method.

        """

        def __call__(*args, **kwargs):
            print("set up action listerner")
            print(self.action_listener)

        return __call__

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)


def Function(func=None, callback_id: Union[str, Pattern] = None):
    if func:
        raise Exception("Missing callback_id")
    else:
        return _Function(func, callback_id)
