from typing import Union, Pattern, Callable, Dict, Optional, Sequence
from logging import Logger

from slack_bolt.listener_matcher import builtins as builtin_matchers

from slack_bolt.response import BoltResponse
from slack_bolt.middleware import Middleware

from slack_bolt.util.utils import extract_listener_callables


class SlackFunction:

    func: Optional[Callable[..., Optional[BoltResponse]]] = None

    def __init__(
        self,
        register_listener: Callable[..., Optional[Callable[..., Optional[BoltResponse]]]],
        base_logger: Logger,
        callback_id: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ):
        self._register_listener = register_listener
        self._base_logger = base_logger
        self.callback_id = callback_id
        self.matchers = matchers
        self.middleware = middleware

    def register_listener(self, *args, **kwargs) -> None:
        functions = extract_listener_callables(kwargs) if kwargs else list(args)
        primary_matcher = builtin_matchers.function_event(callback_id=self.callback_id, base_logger=self._base_logger)
        self.func = self._register_listener(functions, primary_matcher, self.matchers, self.middleware, True)

    def __call__(self, *args, **kwargs) -> Optional[Union[BoltResponse, Callable]]:
        if self.func is not None:
            return self.func(*args, **kwargs)
        self.register_listener(*args, **kwargs)
        return self

    def action(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        """Registers a new action listener to your function. This method can be used as either a decorator or a method.

            # Use this method as a decorator
            @app.function("request-approval")
            def request_approval(event, complete: Complete):
                complete(outputs={})

            @request_approval.action("approve_button")
            def handle_request_approval_events(ack):
                ack()

            # Pass a function to this method
            request_approval_func = app.function("request-approval")(request_approval)
            request_approval.action("approve_button")(handle_request_approval_events)

        * Refer to https://api.slack.com/reference/interaction-payloads/block-actions for actions in `blocks`.

        To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`'s API document.

        Args:
            constraints: The conditions that match a request payload
            matchers: A list of listener matcher functions.
                Only when all the matchers return True, the listener function can be invoked.
            middleware: A list of lister middleware functions.
                Only when all the middleware call `next()` method, the listener function can be invoked.
        """

        def __call__(*args, **kwargs):
            functions = extract_listener_callables(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.function_action(self.callback_id, constraints, base_logger=self._base_logger)
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    # TODO add view listener

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, "__isabstractmethod__", False)
