import logging
from functools import wraps
from logging import Logger
from typing import List, Optional, Union, Callable

from slack_bolt.context.save_thread_context import SaveThreadContext
from slack_bolt.context.assistant.thread_context_store.store import AssistantThreadContextStore
from slack_bolt.listener_matcher.builtins import build_listener_matcher

from slack_bolt.request.request import BoltRequest
from slack_bolt.response.response import BoltResponse
from slack_bolt.listener_matcher import CustomListenerMatcher
from slack_bolt.error import BoltError
from slack_bolt.listener.custom_listener import CustomListener
from slack_bolt.listener import Listener
from slack_bolt.listener.thread_runner import ThreadListenerRunner
from slack_bolt.middleware import Middleware
from slack_bolt.listener_matcher import ListenerMatcher
from slack_bolt.request.payload_utils import (
    is_assistant_thread_started_event,
    is_user_message_event_in_assistant_thread,
    is_assistant_thread_context_changed_event,
    is_other_message_sub_event_in_assistant_thread,
    is_bot_message_event_in_assistant_thread,
)
from slack_bolt.util.utils import is_used_without_argument


class Assistant(Middleware):
    _thread_started_listeners: Optional[List[Listener]]
    _thread_context_changed_listeners: Optional[List[Listener]]
    _user_message_listeners: Optional[List[Listener]]
    _bot_message_listeners: Optional[List[Listener]]

    thread_context_store: Optional[AssistantThreadContextStore]
    base_logger: Optional[logging.Logger]

    def __init__(
        self,
        *,
        app_name: str = "assistant",
        thread_context_store: Optional[AssistantThreadContextStore] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.app_name = app_name
        self.thread_context_store = thread_context_store
        self.base_logger = logger

        self._thread_started_listeners = None
        self._thread_context_changed_listeners = None
        self._user_message_listeners = None
        self._bot_message_listeners = None

    def thread_started(
        self,
        *args,
        matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
        middleware: Optional[Union[Callable, Middleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None,
    ):
        if self._thread_started_listeners is None:
            self._thread_started_listeners = []
        all_matchers = self._merge_matchers(is_assistant_thread_started_event, matchers)
        if is_used_without_argument(args):
            func = args[0]
            self._thread_started_listeners.append(
                self.build_listener(
                    listener_or_functions=func,
                    matchers=all_matchers,
                    middleware=middleware,  # type:ignore[arg-type]
                )
            )
            return func

        def _inner(func):
            functions = [func] + (lazy if lazy is not None else [])
            self._thread_started_listeners.append(
                self.build_listener(
                    listener_or_functions=functions,
                    matchers=all_matchers,
                    middleware=middleware,
                )
            )

            @wraps(func)
            def _wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return _wrapper

        return _inner

    def user_message(
        self,
        *args,
        matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
        middleware: Optional[Union[Callable, Middleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None,
    ):
        if self._user_message_listeners is None:
            self._user_message_listeners = []
        all_matchers = self._merge_matchers(is_user_message_event_in_assistant_thread, matchers)
        if is_used_without_argument(args):
            func = args[0]
            self._user_message_listeners.append(
                self.build_listener(
                    listener_or_functions=func,
                    matchers=all_matchers,
                    middleware=middleware,  # type:ignore[arg-type]
                )
            )
            return func

        def _inner(func):
            functions = [func] + (lazy if lazy is not None else [])
            self._user_message_listeners.append(
                self.build_listener(
                    listener_or_functions=functions,
                    matchers=all_matchers,
                    middleware=middleware,
                )
            )

            @wraps(func)
            def _wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return _wrapper

        return _inner

    def bot_message(
        self,
        *args,
        matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
        middleware: Optional[Union[Callable, Middleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None,
    ):
        if self._bot_message_listeners is None:
            self._bot_message_listeners = []
        all_matchers = self._merge_matchers(is_bot_message_event_in_assistant_thread, matchers)
        if is_used_without_argument(args):
            func = args[0]
            self._bot_message_listeners.append(
                self.build_listener(
                    listener_or_functions=func,
                    matchers=all_matchers,
                    middleware=middleware,  # type:ignore[arg-type]
                )
            )
            return func

        def _inner(func):
            functions = [func] + (lazy if lazy is not None else [])
            self._bot_message_listeners.append(
                self.build_listener(
                    listener_or_functions=functions,
                    matchers=all_matchers,
                    middleware=middleware,
                )
            )

            @wraps(func)
            def _wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return _wrapper

        return _inner

    def thread_context_changed(
        self,
        *args,
        matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
        middleware: Optional[Union[Callable, Middleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None,
    ):
        if self._thread_context_changed_listeners is None:
            self._thread_context_changed_listeners = []
        all_matchers = self._merge_matchers(is_assistant_thread_context_changed_event, matchers)
        if is_used_without_argument(args):
            func = args[0]
            self._thread_context_changed_listeners.append(
                self.build_listener(
                    listener_or_functions=func,
                    matchers=all_matchers,
                    middleware=middleware,  # type:ignore[arg-type]
                )
            )
            return func

        def _inner(func):
            functions = [func] + (lazy if lazy is not None else [])
            self._thread_context_changed_listeners.append(
                self.build_listener(
                    listener_or_functions=functions,
                    matchers=all_matchers,
                    middleware=middleware,
                )
            )

            @wraps(func)
            def _wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return _wrapper

        return _inner

    def _merge_matchers(
        self,
        primary_matcher: Callable[..., bool],
        custom_matchers: Optional[Union[Callable[..., bool], ListenerMatcher]],
    ):
        return [CustomListenerMatcher(app_name=self.app_name, func=primary_matcher)] + (
            custom_matchers or []
        )  # type:ignore[operator]

    @staticmethod
    def default_thread_context_changed(save_thread_context: SaveThreadContext, payload: dict):
        save_thread_context(payload["assistant_thread"]["context"])

    def process(  # type:ignore[return]
        self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse]
    ) -> Optional[BoltResponse]:
        if self._thread_context_changed_listeners is None:
            self.thread_context_changed(self.default_thread_context_changed)

        listener_runner: ThreadListenerRunner = req.context.listener_runner
        for listeners in [
            self._thread_started_listeners,
            self._thread_context_changed_listeners,
            self._user_message_listeners,
            self._bot_message_listeners,
        ]:
            if listeners is not None:
                for listener in listeners:
                    if listener.matches(req=req, resp=resp):
                        return listener_runner.run(
                            request=req,
                            response=resp,
                            listener_name="assistant_listener",
                            listener=listener,
                        )
        if is_other_message_sub_event_in_assistant_thread(req.body):
            # message_changed, message_deleted, etc.
            return req.context.ack()

        next()

    def build_listener(
        self,
        listener_or_functions: Union[Listener, Callable, List[Callable]],
        matchers: Optional[List[Union[ListenerMatcher, Callable[..., bool]]]] = None,
        middleware: Optional[List[Middleware]] = None,
        base_logger: Optional[Logger] = None,
    ) -> Listener:
        if isinstance(listener_or_functions, Callable):  # type:ignore[arg-type]
            listener_or_functions = [listener_or_functions]  # type:ignore[list-item]

        if isinstance(listener_or_functions, Listener):
            return listener_or_functions
        elif isinstance(listener_or_functions, list):
            middleware = middleware if middleware else []
            functions = listener_or_functions
            ack_function = functions.pop(0)

            matchers = matchers if matchers else []
            listener_matchers: List[ListenerMatcher] = []
            for matcher in matchers:
                if isinstance(matcher, ListenerMatcher):
                    listener_matchers.append(matcher)
                elif isinstance(matcher, Callable):  # type:ignore[arg-type]
                    listener_matchers.append(
                        build_listener_matcher(
                            func=matcher,
                            asyncio=False,
                            base_logger=base_logger,
                        )
                    )
            return CustomListener(
                app_name=self.app_name,
                matchers=listener_matchers,
                middleware=middleware,
                ack_function=ack_function,
                lazy_functions=functions,
                auto_acknowledgement=True,
                base_logger=base_logger or self.base_logger,
            )
        else:
            raise BoltError(f"Invalid listener: {type(listener_or_functions)} detected")
