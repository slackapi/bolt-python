import asyncio

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env
from ...adapter_tests.socket_mode.mock_socket_mode_server import (
    start_socket_mode_server,
    stop_socket_mode_server,
)


class TestSocketModeAiohttp:
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    web_client = AsyncWebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)
        try:
            yield  # run the test here
        finally:
            cleanup_mock_web_api_server(self)
            restore_os_env(old_os_env)

    @pytest.mark.asyncio
    async def test_events(self):
        start_socket_mode_server(self, 3021)

        app = AsyncApp(client=self.web_client)

        result = {"shortcut": False, "command": False}

        @app.shortcut("do-something")
        async def shortcut_handler(ack):
            result["shortcut"] = True
            await ack()

        @app.command("/hello-socket-mode")
        async def command_handler(ack):
            result["command"] = True
            await ack()

        handler = AsyncSocketModeHandler(
            app_token="xapp-A111-222-xyz",
            app=app,
        )
        try:
            handler.client.wss_uri = "ws://localhost:3021/link"

            await handler.connect_async()
            await asyncio.sleep(2)  # wait for the message receiver

            await handler.client.send_message("foo")

            await asyncio.sleep(2)
            assert result["shortcut"] is True
            assert result["command"] is True
        finally:
            await handler.client.close()
            stop_socket_mode_server(self)
