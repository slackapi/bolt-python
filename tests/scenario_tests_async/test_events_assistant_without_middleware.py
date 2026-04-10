import asyncio

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.async_app import (
    AsyncApp,
    AsyncBoltContext,
    AsyncBoltRequest,
    AsyncGetThreadContext,
    AsyncSaveThreadContext,
    AsyncSay,
    AsyncSetStatus,
    AsyncSetSuggestedPrompts,
    AsyncSetTitle,
)
from tests.mock_web_api_server import cleanup_mock_web_api_server_async, setup_mock_web_api_server_async
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
        listener_called = asyncio.Event()

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
            listener_called.set()

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_thread_context_changed(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

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
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            listener_called.set()

        request = AsyncBoltRequest(body=thread_context_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_user_message(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

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
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            try:
                await set_status("is typing...")
                await say("Here you are!")
                listener_called.set()
            except Exception as e:
                await say(f"Oops, something went wrong (error: {e})")

        request = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_user_message_with_assistant_thread(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

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
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            try:
                await set_status("is typing...")
                await say("Here you are!")
                listener_called.set()
            except Exception as e:
                await say(f"Oops, something went wrong (error: {e})")

        request = AsyncBoltRequest(body=user_message_event_body_with_assistant_thread, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_message_changed(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

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
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == None
            assert set_status is not None
            assert set_title is None
            assert set_suggested_prompts is None
            assert get_thread_context is None
            assert save_thread_context is None
            listener_called.set()

        request = AsyncBoltRequest(body=message_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_channel_user_message(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

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
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == None
            assert set_status is not None
            assert set_title is None
            assert set_suggested_prompts is None
            assert get_thread_context is None
            assert save_thread_context is None
            listener_called.set()

        request = AsyncBoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_channel_message_changed(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

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
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == None
            assert set_status is not None
            assert set_title is None
            assert set_suggested_prompts is None
            assert get_thread_context is None
            assert save_thread_context is None
            listener_called.set()

        request = AsyncBoltRequest(body=channel_message_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_assistant_events_conversation_kwargs_disabled(self):
        app = AsyncApp(client=self.web_client, attaching_conversation_kwargs_enabled=False)

        listener_called = asyncio.Event()

        @app.event("assistant_thread_started")
        async def start_thread(context: AsyncBoltContext):
            assert context.get("set_status") is None
            assert context.get("set_title") is None
            assert context.get("set_suggested_prompts") is None
            assert context.get("get_thread_context") is None
            assert context.get("save_thread_context") is None
            listener_called.set()

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True
