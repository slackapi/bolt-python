import asyncio
import time

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.say.async_say import AsyncSay
from slack_bolt.context.set_status.async_set_status import AsyncSetStatus
from slack_bolt.context.set_title.async_set_title import AsyncSetTitle
from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from slack_bolt.context.get_thread_context.async_get_thread_context import AsyncGetThreadContext
from slack_bolt.context.save_thread_context.async_save_thread_context import AsyncSaveThreadContext
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server_async,
    setup_mock_web_api_server_async,
)
from tests.scenario_tests_async.test_events_assistant import (
    channel_message_changed_event_body,
    channel_user_message_event_body,
    message_changed_event_body,
    thread_context_changed_event_body,
    thread_started_event_body,
    user_message_event_body,
    user_message_event_body_with_assistant_thread,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


async def assert_target_called(called: dict, timeout: float = 2.0):
    deadline = time.time() + timeout
    while called["value"] is False and time.time() < deadline:
        await asyncio.sleep(0.1)
    assert called["value"] is True


class TestAsyncEventsAssistantWithoutMiddleware:
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
    async def test_thread_started(self):
        app = AsyncApp(client=self.web_client)
        called = {"value": False}

        @app.event("assistant_thread_started")
        async def handle_assistant_thread_started(
            say: AsyncSay,
            set_status: AsyncSetStatus,
            set_title: AsyncSetTitle,
            set_suggested_prompts: AsyncSetSuggestedPrompts,
            get_thread_context: AsyncGetThreadContext,
            save_thread_context: AsyncSaveThreadContext,
            context: AsyncBoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            await say("Hi, how can I help you today?")
            await set_suggested_prompts(
                prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}]
            )
            called["value"] = True

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_target_called(called)

    @pytest.mark.asyncio
    async def test_thread_context_changed(self):
        app = AsyncApp(client=self.web_client)
        called = {"value": False}

        @app.event("assistant_thread_context_changed")
        async def handle_assistant_thread_context_changed(
            say: AsyncSay,
            set_status: AsyncSetStatus,
            set_title: AsyncSetTitle,
            set_suggested_prompts: AsyncSetSuggestedPrompts,
            get_thread_context: AsyncGetThreadContext,
            save_thread_context: AsyncSaveThreadContext,
            context: AsyncBoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say is not None
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            called["value"] = True

        request = AsyncBoltRequest(body=thread_context_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_target_called(called)

    @pytest.mark.asyncio
    async def test_user_message(self):
        app = AsyncApp(client=self.web_client)
        called = {"value": False}

        @app.message("")
        async def handle_message(
            say: AsyncSay,
            set_status: AsyncSetStatus,
            set_title: AsyncSetTitle,
            set_suggested_prompts: AsyncSetSuggestedPrompts,
            get_thread_context: AsyncGetThreadContext,
            save_thread_context: AsyncSaveThreadContext,
            context: AsyncBoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            try:
                await set_status("is typing...")
                await say("Here you are!")
                called["value"] = True
            except Exception as e:
                await say(f"Oops, something went wrong (error: {e}")

        request = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_target_called(called)

    @pytest.mark.asyncio
    async def test_user_message_with_assistant_thread(self):
        app = AsyncApp(client=self.web_client)
        called = {"value": False}

        @app.message("")
        async def handle_message(
            say: AsyncSay,
            set_status: AsyncSetStatus,
            set_title: AsyncSetTitle,
            set_suggested_prompts: AsyncSetSuggestedPrompts,
            get_thread_context: AsyncGetThreadContext,
            save_thread_context: AsyncSaveThreadContext,
            context: AsyncBoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            try:
                await set_status("is typing...")
                await say("Here you are!")
                called["value"] = True
            except Exception as e:
                await say(f"Oops, something went wrong (error: {e}")

        request = AsyncBoltRequest(body=user_message_event_body_with_assistant_thread, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_target_called(called)

    @pytest.mark.asyncio
    async def test_message_changed(self):
        app = AsyncApp(client=self.web_client)

        @app.event("message")
        async def handle_message_event(
            say: AsyncSay,
            set_status: AsyncSetStatus,
            set_title: AsyncSetTitle,
            set_suggested_prompts: AsyncSetSuggestedPrompts,
            get_thread_context: AsyncGetThreadContext,
            save_thread_context: AsyncSaveThreadContext,
            context: AsyncBoltContext,
        ):
            assert context.thread_ts is not None
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None

        request = AsyncBoltRequest(body=message_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200

    @pytest.mark.asyncio
    async def test_channel_user_message(self):
        app = AsyncApp(client=self.web_client)

        @app.event("message")
        async def handle_message_event(
            say: AsyncSay,
            set_status: AsyncSetStatus,
            set_title: AsyncSetTitle,
            set_suggested_prompts: AsyncSetSuggestedPrompts,
            get_thread_context: AsyncGetThreadContext,
            save_thread_context: AsyncSaveThreadContext,
            context: AsyncBoltContext,
        ):
            assert context.thread_ts is not None
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None

        request = AsyncBoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200

    @pytest.mark.asyncio
    async def test_channel_message_changed(self):
        app = AsyncApp(client=self.web_client)

        @app.event("message")
        async def handle_message_event(
            say: AsyncSay,
            set_status: AsyncSetStatus,
            set_title: AsyncSetTitle,
            set_suggested_prompts: AsyncSetSuggestedPrompts,
            get_thread_context: AsyncGetThreadContext,
            save_thread_context: AsyncSaveThreadContext,
            context: AsyncBoltContext,
        ):
            assert context.thread_ts is not None
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None

        request = AsyncBoltRequest(body=channel_message_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
