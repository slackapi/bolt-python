from typing import Callable

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck

from slack_bolt import BoltResponse
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class NoopAsyncAck(AsyncAck):
    async def __call__(self) -> BoltResponse:
        pass


class TestAppDecorators:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    web_client = AsyncWebClient(token=valid_token, base_url=mock_api_server_base_url)

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    @pytest.mark.asyncio
    async def test_decorators(self):
        app = AsyncApp(signing_secret=self.signing_secret, client=self.web_client)
        ack = NoopAsyncAck()

        @app.function("c")
        async def handle_function_events(body: dict):
            assert body is not None

        @handle_function_events.action("some-func-action-id")
        async def handle_function_action(ack: AsyncAck, body: dict):
            assert body is not None
            await ack()

        await handle_function_action(ack, {})
        assert isinstance(handle_function_action, Callable)

        @handle_function_events.view("some-callback-id")
        async def handle_views(ack: AsyncAck, body: dict):
            assert body is not None
            await ack()

        await handle_views(ack, {})
        assert isinstance(handle_views, Callable)

        await handle_function_events({})
        assert isinstance(handle_function_events, Callable)

    @pytest.mark.asyncio
    async def test_initialized_decorators(self):
        app = AsyncApp(signing_secret=self.signing_secret, client=self.web_client)
        ack = NoopAsyncAck()

        func = app.function("c")

        @func
        async def handle_function_events(body: dict):
            assert body is not None

        @handle_function_events.action("some-func-action-id")
        async def handle_function_action(ack: AsyncAck, body: dict):
            assert body is not None
            await ack()

        await handle_function_action(ack, {})
        assert isinstance(handle_function_action, Callable)

        await handle_function_events({})
        assert isinstance(handle_function_events, Callable)

    @pytest.mark.asyncio
    async def test_mixed_decorators(self):
        app = AsyncApp(signing_secret=self.signing_secret, client=self.web_client)
        ack = NoopAsyncAck()

        func = app.function("c")

        @func
        async def handle_function_events(body: dict):
            assert body is not None

        @func.action("some-func-action-id")
        async def handle_function_action(ack: AsyncAck, body: dict):
            assert body is not None
            await ack()

        await handle_function_action(ack, {})
        assert isinstance(handle_function_action, Callable)

        await handle_function_events({})
        assert isinstance(handle_function_events, Callable)
