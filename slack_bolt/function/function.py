from typing import List, Union, Pattern, Callable, Dict, Optional, Sequence
from logging import Logger

from slack_bolt.listener_matcher import builtins as builtin_matchers

from slack_bolt.response import BoltResponse
from slack_bolt.middleware import Middleware
from slack_bolt.middleware.function_token import FunctionToken

from slack_bolt.util.utils import to_listener_functions


class Function:

    func: Optional[Callable[..., Optional[BoltResponse]]] = None

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
        self.func = self._register_listener(functions, primary_matcher, matchers, middleware, True)
        return self

    def __call__(self, *args, **kwargs) -> Optional[BoltResponse]:
        if self.func is not None:
            return self.func(*args, **kwargs)
        return None

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        """Registers a new action listener to your function. This method can be used as either a decorator or a method.

            @app.function("reverse")
            def reverse_string(event, complete_success: CompleteSuccess, complete_error: CompleteError):
                complete_error("There is no error")

            # Use this method as a decorator
            @reverse_string.action("approve_button")
            def update_message(ack):
                ack()

            # Pass a function to this method
            reverse_string.action("approve_button")(update_message)

        * Refer to https://api.slack.com/reference/interaction-payloads/block-actions for actions in `blocks`.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`'s API document.

        Args:
            constraints: The conditions that match a request payload
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """

        middleware = list(middleware) if middleware else []
        middleware.insert(0, FunctionToken())

        def __call__(*args, **kwargs):
            functions = to_listener_functions(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.function_action(self.callback_id, constraints, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, "__isabstractmethod__", False)
