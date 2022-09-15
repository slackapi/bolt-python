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
        callback_id: str,
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
        asyncio: bool = False,
    ):
        self._register_listener = register_listener
        self._base_logger = base_logger
        self.callback_id = callback_id
        self.matchers = matchers
        self.middleware = middleware
        self.asyncio = asyncio

    def register_listener(self, *args, **kwargs) -> None:
        functions = extract_listener_callables(kwargs) if kwargs else list(args)
        primary_matcher = builtin_matchers.function_event(
            callback_id=self.callback_id, base_logger=self._base_logger, asyncio=self.asyncio
        )
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

            # Define a function handler using the function decorator
            @app.function("request-approval")
            def request_approval(event, complete: Complete):
                # do something

            @request_approval.action("approve_button")
            def handle_request_approval_events(ack, complete):
                ack()
                complete()

            # Pass a function to this method
            request_approval_func = app.function("request-approval")(request_approval)
            request_approval.action("approve_button")(handle_request_approval_events)

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
            primary_matcher = builtin_matchers.function_action(
                self.callback_id, constraints, base_logger=self._base_logger, asyncio=self.asyncio
            )
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    # -------------------------
    # view

    def view(
        self,
        constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        """Registers a new `view_submission`/`view_closed` event listener for a function.

            # Define a function handler using the function decorator
            @app.function("function_1")
            def sample_view(event, complete: Complete):
                # Assume there's an interactivity object passed in as input `interactivity`
                interactivity_pointer = event["inputs"]["interactivity"]["interactivity_pointer"]
                client.views_open(
                    interactivity_pointer=interactivity_pointer,
                    view={...}
                )

            # Use this method as a decorator
            @sample_view.view("view_1")
            def handle_submission(ack, body, client, view, complete):
                # Assume there's an input block with `block_c` as the block_id and `dreamy_input`
                hopes_and_dreams = view["state"]["values"]["block_c"]["dreamy_input"]
                user = body["user"]["id"]
                # Validate the inputs
                errors = {}
                if hopes_and_dreams is not None and len(hopes_and_dreams) <= 5:
                    errors["block_c"] = "The value must be longer than 5 characters"
                if len(errors) > 0:
                    ack(response_action="errors", errors=errors)
                    return
                # Acknowledge the view_submission event and close the modal
                ack()
                # complete the function
                complete()

            # Pass a function to this method
            sample_view_func = app.function("request-approval")(sample_view)
            sample_view_func.view("view_1")(handle_submission)

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
            primary_matcher = builtin_matchers.function_view(
                self.callback_id, constraints, base_logger=self._base_logger, asyncio=self.asyncio
            )
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def view_submission(
        self,
        constraints: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        """Registers a new `view_submission` listener."""

        def __call__(*args, **kwargs):
            functions = extract_listener_callables(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.function_view_submission(
                self.callback_id, constraints, base_logger=self._base_logger, asyncio=self.asyncio
            )
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__

    def view_closed(
        self,
        constraints: Union[str, Pattern],
        matchers: Optional[Sequence[Callable[..., bool]]] = None,
        middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    ) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]:
        """Registers a new `view_closed` listener."""

        def __call__(*args, **kwargs):
            functions = extract_listener_callables(kwargs) if kwargs else list(args)
            primary_matcher = builtin_matchers.function_view_closed(
                self.callback_id, constraints, base_logger=self._base_logger, asyncio=self.asyncio
            )
            return self._register_listener(list(functions), primary_matcher, matchers, middleware)

        return __call__
