import logging
from functools import wraps
from logging import Logger
from typing import List, Optional, Union, Callable, Awaitable

from slack_bolt.context.save_thread_context.async_save_thread_context import AsyncSaveThreadContext
from slack_bolt.context.assistant.thread_context_store.async_store import AsyncAssistantThreadContextStore

from slack_bolt.listener.asyncio_runner import AsyncioListenerRunner
from slack_bolt.listener_matcher.builtins import build_listener_matcher
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from slack_bolt.error import BoltError
from slack_bolt.listener.async_listener import AsyncListener, AsyncCustomListener
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.listener_matcher.async_listener_matcher import AsyncListenerMatcher
from slack_bolt.request.payload_utils import (
    is_assistant_thread_started_event,
    is_user_message_event_in_assistant_thread,
    is_assistant_thread_context_changed_event,
    is_other_message_sub_event_in_assistant_thread,
    is_bot_message_event_in_assistant_thread,
)
from slack_bolt.util.utils import is_used_without_argument


class AsyncAssistant(AsyncMiddleware):
    _thread_started_listeners: Optional[List[AsyncListener]]
    _user_message_listeners: Optional[List[AsyncListener]]
    _bot_message_listeners: Optional[List[AsyncListener]]
    _thread_context_changed_listeners: Optional[List[AsyncListener]]

    thread_context_store: Optional[AsyncAssistantThreadContextStore]
    base_logger: Optional[logging.Logger]

    def __init__(
        self,
        *,
        app_name: str = "assistant",
        thread_context_store: Optional[AsyncAssistantThreadContextStore] = None,
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
        matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]] = None,
        middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None,
    ):
        if self._thread_started_listeners is None:
            self._thread_started_listeners = []
        all_matchers = self._merge_matchers(
            build_listener_matcher(
                func=is_assistant_thread_started_event,
                asyncio=True,
                base_logger=self.base_logger,
            ),  # type:ignore[arg-type]
            matchers,
        )
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
        matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]] = None,
        middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None,
    ):
        if self._user_message_listeners is None:
            self._user_message_listeners = []
        all_matchers = self._merge_matchers(
            build_listener_matcher(
                func=is_user_message_event_in_assistant_thread,
                asyncio=True,
                base_logger=self.base_logger,
            ),  # type:ignore[arg-type]
            matchers,
        )
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
        matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]] = None,
        middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None,
    ):
        if self._bot_message_listeners is None:
            self._bot_message_listeners = []
        all_matchers = self._merge_matchers(
            build_listener_matcher(
                func=is_bot_message_event_in_assistant_thread,
                asyncio=True,
                base_logger=self.base_logger,
            ),  # type:ignore[arg-type]
            matchers,
        )
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
        matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]] = None,
        middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None,
    ):
        if self._thread_context_changed_listeners is None:
            self._thread_context_changed_listeners = []
        all_matchers = self._merge_matchers(
            build_listener_matcher(
                func=is_assistant_thread_context_changed_event,
                asyncio=True,
                base_logger=self.base_logger,
            ),  # type:ignore[arg-type]
            matchers,
        )
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

    @staticmethod
    def _merge_matchers(
        primary_matcher: Union[Callable[..., bool], AsyncListenerMatcher],
        custom_matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]],
    ):
        return [primary_matcher] + (custom_matchers or [])  # type:ignore[operator]

    @staticmethod
    async def default_thread_context_changed(save_thread_context: AsyncSaveThreadContext, payload: dict):
        new_context: dict = payload["assistant_thread"]["context"]
        await save_thread_context(new_context)

    async def async_process(  # type:ignore[return]
        self,
        *,
        req: AsyncBoltRequest,
        resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]],
    ) -> Optional[BoltResponse]:
        if self._thread_context_changed_listeners is None:
            self.thread_context_changed(self.default_thread_context_changed)

        listener_runner: AsyncioListenerRunner = req.context.listener_runner
        for listeners in [
            self._thread_started_listeners,
            self._thread_context_changed_listeners,
            self._user_message_listeners,
            self._bot_message_listeners,
        ]:
            if listeners is not None:
                for listener in listeners:
                    if listener is not None and await listener.async_matches(req=req, resp=resp):
                        return await listener_runner.run(
                            request=req,
                            response=resp,
                            listener_name="assistant_listener",
                            listener=listener,
                        )
        if is_other_message_sub_event_in_assistant_thread(req.body):
            # message_changed, message_deleted, etc.
            return await req.context.ack()

        await next()

    def build_listener(
        self,
        listener_or_functions: Union[AsyncListener, Callable, List[Callable]],
        matchers: Optional[List[Union[AsyncListenerMatcher, Callable[..., Awaitable[bool]]]]] = None,
        middleware: Optional[List[AsyncMiddleware]] = None,
        base_logger: Optional[Logger] = None,
    ) -> AsyncListener:
        if isinstance(listener_or_functions, Callable):  # type:ignore[arg-type]
            listener_or_functions = [listener_or_functions]  # type:ignore[list-item]

        if isinstance(listener_or_functions, AsyncListener):
            return listener_or_functions
        elif isinstance(listener_or_functions, list):
            middleware = middleware if middleware else []
            functions = listener_or_functions
            ack_function = functions.pop(0)

            matchers = matchers if matchers else []
            listener_matchers: List[AsyncListenerMatcher] = []
            for matcher in matchers:
                if isinstance(matcher, AsyncListenerMatcher):
                    listener_matchers.append(matcher)
                else:
                    listener_matchers.append(
                        build_listener_matcher(
                            func=matcher,  # type:ignore[arg-type]
                            asyncio=True,
                            base_logger=base_logger,
                        )
                    )
            return AsyncCustomListener(
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
