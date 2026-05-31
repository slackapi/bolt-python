from typing import Awaitable, Callable, Optional

import pytest
from slack_sdk import WebClient
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt import App, Assistant, BoltRequest
from slack_bolt.async_app import AsyncApp, AsyncAssistant, AsyncBoltRequest
from slack_bolt.authorization import AuthorizeResult
from slack_bolt.middleware import Middleware
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.request import BoltRequest as BoltRequestType
from slack_bolt.response import BoltResponse
from tests.scenario_tests.test_events_assistant import thread_started_event_body, user_message_event_body


def authorize_test_app(context, enterprise_id, team_id, user_id):
    return AuthorizeResult(
        enterprise_id=enterprise_id,
        team_id=team_id,
        user_id=user_id,
        bot_user_id="W111",
        bot_id="B111",
        bot_token="xoxb-valid",
    )


async def async_authorize_test_app(context, enterprise_id, team_id, user_id):
    return authorize_test_app(context, enterprise_id, team_id, user_id)


class TestAppAssistantMiddleware:
    def test_assistant_inherits_app_middleware_registered_after_assistant(self):
        app = App(client=WebClient(token=None), authorize=authorize_test_app, process_before_response=True)
        assistant = Assistant(auto_inherit_app_middleware=True)
        calls = []

        class ListenerMiddleware(Middleware):
            def process(self, *, req: BoltRequestType, resp: BoltResponse, next: Callable[[], BoltResponse]):
                calls.append("listener")
                return next()

        @assistant.user_message(middleware=[ListenerMiddleware()])
        def handle_user_message():
            calls.append("handler")

        app.assistant(assistant)

        @app.middleware
        def app_middleware(req, next):
            calls.append("app")
            assert req.context.get("set_status") is not None
            assert req.context.get("set_title") is not None
            return next()

        request = BoltRequest(body=user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert calls == ["app", "listener", "handler"]

    def test_assistant_does_not_inherit_app_middleware_by_default(self):
        app = App(client=WebClient(token=None), authorize=authorize_test_app, process_before_response=True)
        assistant = Assistant()
        calls = []

        class AppMiddleware(Middleware):
            def process(self, *, req: BoltRequestType, resp: BoltResponse, next: Callable[[], BoltResponse]):
                calls.append("app")
                return next()

        @assistant.user_message
        def handle_user_message():
            calls.append("handler")

        app.assistant(assistant)
        app.middleware(AppMiddleware())

        request = BoltRequest(body=user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert calls == ["handler"]

    def test_assistant_inherits_app_middleware_for_listeners_registered_later(self):
        app = App(client=WebClient(token=None), authorize=authorize_test_app, process_before_response=True)
        assistant = Assistant(auto_inherit_app_middleware=True)
        calls = []

        class AppMiddleware(Middleware):
            def process(self, *, req: BoltRequestType, resp: BoltResponse, next: Callable[[], BoltResponse]):
                calls.append("app")
                return next()

        app.assistant(assistant)
        app.middleware(AppMiddleware())

        @assistant.user_message
        def handle_user_message():
            calls.append("handler")

        request = BoltRequest(body=user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert calls == ["app", "handler"]

    def test_assistant_inherited_app_middleware_can_short_circuit(self):
        app = App(client=WebClient(token=None), authorize=authorize_test_app, process_before_response=True)
        assistant = Assistant(auto_inherit_app_middleware=True)
        calls = []

        class BlockingMiddleware(Middleware):
            def process(self, *, req: BoltRequestType, resp: BoltResponse, next: Callable[[], BoltResponse]):
                calls.append("app")
                return BoltResponse(status=201)

        @assistant.thread_started
        def start_thread():
            calls.append("handler")

        app.assistant(assistant)
        app.middleware(BlockingMiddleware())

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 201
        assert calls == ["app"]


class TestAsyncAppAssistantMiddleware:
    @pytest.mark.asyncio
    async def test_assistant_inherits_app_middleware_registered_after_assistant(self):
        app = AsyncApp(client=AsyncWebClient(token=None), authorize=async_authorize_test_app, process_before_response=True)
        assistant = AsyncAssistant(auto_inherit_app_middleware=True)
        calls = []

        class ListenerMiddleware(AsyncMiddleware):
            async def async_process(
                self,
                *,
                req: AsyncBoltRequest,
                resp: BoltResponse,
                next: Callable[[], Awaitable[BoltResponse]],
            ) -> Optional[BoltResponse]:
                calls.append("listener")
                return await next()

        @assistant.user_message(middleware=[ListenerMiddleware()])
        async def handle_user_message():
            calls.append("handler")

        app.assistant(assistant)

        @app.middleware
        async def app_middleware(req, next):
            calls.append("app")
            assert req.context.get("set_status") is not None
            assert req.context.get("set_title") is not None
            return await next()

        request = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert calls == ["app", "listener", "handler"]

    @pytest.mark.asyncio
    async def test_assistant_does_not_inherit_app_middleware_by_default(self):
        app = AsyncApp(client=AsyncWebClient(token=None), authorize=async_authorize_test_app, process_before_response=True)
        assistant = AsyncAssistant()
        calls = []

        class AppMiddleware(AsyncMiddleware):
            async def async_process(
                self,
                *,
                req: AsyncBoltRequest,
                resp: BoltResponse,
                next: Callable[[], Awaitable[BoltResponse]],
            ) -> Optional[BoltResponse]:
                calls.append("app")
                return await next()

        @assistant.user_message
        async def handle_user_message():
            calls.append("handler")

        app.assistant(assistant)
        app.middleware(AppMiddleware())

        request = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert calls == ["handler"]

    @pytest.mark.asyncio
    async def test_assistant_inherits_app_middleware_for_listeners_registered_later(self):
        app = AsyncApp(client=AsyncWebClient(token=None), authorize=async_authorize_test_app, process_before_response=True)
        assistant = AsyncAssistant(auto_inherit_app_middleware=True)
        calls = []

        class AppMiddleware(AsyncMiddleware):
            async def async_process(
                self,
                *,
                req: AsyncBoltRequest,
                resp: BoltResponse,
                next: Callable[[], Awaitable[BoltResponse]],
            ) -> Optional[BoltResponse]:
                calls.append("app")
                return await next()

        app.assistant(assistant)
        app.middleware(AppMiddleware())

        @assistant.user_message
        async def handle_user_message():
            calls.append("handler")

        request = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert calls == ["app", "handler"]

    @pytest.mark.asyncio
    async def test_assistant_inherited_app_middleware_can_short_circuit(self):
        app = AsyncApp(client=AsyncWebClient(token=None), authorize=async_authorize_test_app, process_before_response=True)
        assistant = AsyncAssistant(auto_inherit_app_middleware=True)
        calls = []

        class BlockingMiddleware(AsyncMiddleware):
            async def async_process(
                self,
                *,
                req: AsyncBoltRequest,
                resp: BoltResponse,
                next: Callable[[], Awaitable[BoltResponse]],
            ) -> Optional[BoltResponse]:
                calls.append("app")
                return BoltResponse(status=201)

        @assistant.thread_started
        async def start_thread():
            calls.append("handler")

        app.assistant(assistant)
        app.middleware(BlockingMiddleware())

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 201
        assert calls == ["app"]
