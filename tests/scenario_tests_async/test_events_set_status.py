import asyncio
import json
from urllib.parse import quote

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.async_app import AsyncAssistant
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.set_status.async_set_status import AsyncSetStatus
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import (
    assert_auth_test_count_async,
    assert_received_request_count_async,
    cleanup_mock_web_api_server_async,
    setup_mock_web_api_server_async,
)
from tests.scenario_tests_async.test_app import app_mention_event_body
from tests.scenario_tests_async.test_events_assistant import thread_started_event_body
from tests.scenario_tests_async.test_events_assistant import user_message_event_body as threaded_user_message_event_body
from tests.scenario_tests_async.test_message_bot import bot_message_event_payload, user_message_event_payload
from tests.scenario_tests_async.test_view_submission import body as view_submission_body
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncEventsSetStatus:
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    web_client = AsyncWebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server_async(self)
        try:
            yield
        finally:
            cleanup_mock_web_api_server_async(self)
            restore_os_env(old_os_env)

    @pytest.mark.asyncio
    async def test_set_status_injected_for_app_mention(self):
        app = AsyncApp(client=self.web_client)

        @app.event("app_mention")
        async def handle_mention(set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert set_status is not None
            assert isinstance(set_status, AsyncSetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "C111"
            assert set_status.thread_ts == "1595926230.009600"
            await set_status(status="Thinking...")

        request = AsyncBoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, path="/assistant.threads.setStatus", min_count=1)

    @pytest.mark.asyncio
    async def test_set_status_injected_for_threaded_message(self):
        app = AsyncApp(client=self.web_client)

        @app.event("message")
        async def handle_message(set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert set_status is not None
            assert isinstance(set_status, AsyncSetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "D111"
            assert set_status.thread_ts == "1726133698.626339"
            await set_status(status="Thinking...")

        request = AsyncBoltRequest(body=threaded_user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, path="/assistant.threads.setStatus", min_count=1)

    @pytest.mark.asyncio
    async def test_set_status_in_user_message(self):
        app = AsyncApp(client=self.web_client)

        @app.message("")
        async def handle_user_message(set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert set_status is not None
            assert isinstance(set_status, AsyncSetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "C111"
            assert set_status.thread_ts == "1610261659.001400"
            await set_status(status="Thinking...")

        request = AsyncBoltRequest(body=user_message_event_payload, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, path="/assistant.threads.setStatus", min_count=1)

    @pytest.mark.asyncio
    async def test_set_status_in_bot_message(self):
        app = AsyncApp(client=self.web_client)

        @app.message("")
        async def handle_user_message(set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert set_status is not None
            assert isinstance(set_status, AsyncSetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "C111"
            assert set_status.thread_ts == "1610261539.000900"
            await set_status(status="Thinking...")

        request = AsyncBoltRequest(body=bot_message_event_payload, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, path="/assistant.threads.setStatus", min_count=1)

    @pytest.mark.asyncio
    async def test_set_status_in_assistant_thread_started(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()

        @assistant.thread_started
        async def start_thread(set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert set_status is not None
            assert isinstance(set_status, AsyncSetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "D111"
            assert set_status.thread_ts == "1726133698.626339"
            await set_status(status="Thinking...")

        app.assistant(assistant)

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, path="/assistant.threads.setStatus", min_count=1)

    @pytest.mark.asyncio
    async def test_set_status_in_assistant_user_message(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()

        @assistant.user_message
        async def handle_user_message(set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert set_status is not None
            assert isinstance(set_status, AsyncSetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "D111"
            assert set_status.thread_ts == "1726133698.626339"
            await set_status(status="Thinking...")

        app.assistant(assistant)

        request = AsyncBoltRequest(body=threaded_user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, path="/assistant.threads.setStatus", min_count=1)

    @pytest.mark.asyncio
    async def test_set_status_is_none_for_view_submission(self):
        app = AsyncApp(client=self.web_client, request_verification_enabled=False)
        listener_called = asyncio.Event()

        @app.view("view-id")
        async def handle_view(ack, set_status, context: AsyncBoltContext):
            await ack()
            assert set_status is None
            assert context.set_status is None
            listener_called.set()

        request = AsyncBoltRequest(
            body=f"payload={quote(json.dumps(view_submission_body))}",
        )
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        assert listener_called.is_set()
