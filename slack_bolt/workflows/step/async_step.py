from typing import Callable, Union, Optional, Awaitable, Sequence

from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.listener.async_listener import AsyncListener, AsyncCustomListener
from slack_bolt.listener_matcher.builtins import (
    workflow_step_edit,
    workflow_step_save,
    workflow_step_execute,
)
from slack_bolt.middleware.async_custom_middleware import AsyncCustomMiddleware
from slack_bolt.response import BoltResponse
from slack_sdk.web.async_client import AsyncWebClient
from .utilities.async_configure import AsyncConfigure
from .utilities.async_fail import AsyncFail
from .utilities.async_complete import AsyncComplete
from .utilities.async_update import AsyncUpdate
from ...listener_matcher.async_listener_matcher import AsyncListenerMatcher
from ...middleware.async_middleware import AsyncMiddleware


class AsyncWorkflowStep:
    callback_id: str
    edit: AsyncListener
    save: AsyncListener
    execute: AsyncListener

    def __init__(
        self,
        *,
        callback_id: str,
        edit: Union[
            Callable[..., Awaitable[BoltResponse]], AsyncListener, Sequence[Callable]
        ],
        save: Union[
            Callable[..., Awaitable[BoltResponse]], AsyncListener, Sequence[Callable]
        ],
        execute: Union[
            Callable[..., Awaitable[BoltResponse]], AsyncListener, Sequence[Callable]
        ],
        app_name: Optional[str] = None,
    ):
        self.callback_id = callback_id
        app_name = app_name or __name__
        self.edit = self._build_listener(callback_id, app_name, edit, "edit")
        self.save = self._build_listener(callback_id, app_name, save, "save")
        self.execute = self._build_listener(callback_id, app_name, execute, "execute")

    @classmethod
    def _build_listener(
        cls,
        callback_id: str,
        app_name: str,
        listener: AsyncListener,
        name: str,
    ) -> AsyncListener:
        if isinstance(listener, AsyncListener):
            return listener
        elif isinstance(listener, Callable):
            return AsyncCustomListener(
                app_name=app_name,
                matchers=cls._build_matchers(name, callback_id),
                middleware=cls._build_middleware(name, callback_id),
                ack_function=listener,
                lazy_functions=[],
                auto_acknowledgement=name == "execute",
            )
        elif isinstance(listener, list) and len(listener) > 0:
            ack = listener.pop(0)
            lazy = listener
            return AsyncCustomListener(
                app_name=app_name,
                matchers=cls._build_matchers(name, callback_id),
                middleware=cls._build_middleware(name, callback_id),
                ack_function=ack,
                lazy_functions=lazy,
                auto_acknowledgement=name == "execute",
            )
        else:
            raise ValueError(f"Invalid `{name}` listener")

    @classmethod
    def _build_matchers(
        cls, name: str, callback_id: str
    ) -> Sequence[AsyncListenerMatcher]:
        if name == "edit":
            return [workflow_step_edit(callback_id, asyncio=True)]
        elif name == "save":
            return [workflow_step_save(callback_id, asyncio=True)]
        elif name == "execute":
            return [workflow_step_execute(callback_id, asyncio=True)]
        else:
            raise ValueError(f"Invalid name {name}")

    @classmethod
    def _build_middleware(
        cls, name: str, callback_id: str
    ) -> Sequence[AsyncMiddleware]:
        if name == "edit":
            return [_build_edit_listener_middleware(callback_id)]
        elif name == "save":
            return [_build_save_listener_middleware()]
        elif name == "execute":
            return [_build_execute_listener_middleware()]
        else:
            raise ValueError(f"Invalid name {name}")


#######################
# Edit
#######################


def _build_edit_listener_middleware(callback_id: str) -> AsyncMiddleware:
    async def edit_listener_middleware(
        context: AsyncBoltContext,
        client: AsyncWebClient,
        body: dict,
        next: Callable[[], Awaitable[BoltResponse]],
    ):
        context["configure"] = AsyncConfigure(
            callback_id=callback_id,
            client=client,
            body=body,
        )
        return await next()

    return AsyncCustomMiddleware(app_name=__name__, func=edit_listener_middleware)


#######################
# Save
#######################


def _build_save_listener_middleware() -> AsyncMiddleware:
    async def save_listener_middleware(
        context: AsyncBoltContext,
        client: AsyncWebClient,
        body: dict,
        next: Callable[[], Awaitable[BoltResponse]],
    ):
        context["update"] = AsyncUpdate(
            client=client,
            body=body,
        )
        return await next()

    return AsyncCustomMiddleware(app_name=__name__, func=save_listener_middleware)


#######################
# Execute
#######################


def _build_execute_listener_middleware() -> AsyncMiddleware:
    async def execute_listener_middleware(
        context: AsyncBoltContext,
        client: AsyncWebClient,
        body: dict,
        next: Callable[[], Awaitable[BoltResponse]],
    ):
        context["complete"] = AsyncComplete(
            client=client,
            body=body,
        )
        context["fail"] = AsyncFail(
            client=client,
            body=body,
        )
        return await next()

    return AsyncCustomMiddleware(app_name=__name__, func=execute_listener_middleware)
