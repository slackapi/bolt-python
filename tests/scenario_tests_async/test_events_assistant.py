import asyncio
from typing import Awaitable, Callable, Optional

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.async_app import (
    AsyncApp,
    AsyncAssistant,
    AsyncBoltContext,
    AsyncBoltRequest,
    AsyncSay,
    AsyncSetStatus,
    AsyncSetSuggestedPrompts,
)
from slack_bolt.middleware.async_middleware import AsyncMiddleware
from slack_bolt.response import BoltResponse
from tests.mock_web_api_server import cleanup_mock_web_api_server_async, setup_mock_web_api_server_async
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncEventsAssistant:
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
            yield  # run the test here
        finally:
            cleanup_mock_web_api_server_async(self)
            restore_os_env(old_os_env)

    @pytest.mark.asyncio
    async def test_thread_started(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.thread_started
        async def start_thread(
            say: AsyncSay,
            set_suggested_prompts: AsyncSetSuggestedPrompts,
            set_status: AsyncSetStatus,
            context: AsyncBoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert set_status.thread_ts == context.thread_ts
            assert say.thread_ts == context.thread_ts
            await say("Hi, how can I help you today?")
            await set_suggested_prompts(
                prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}]
            )
            await set_suggested_prompts(
                prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}],
                title="foo",
            )
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_thread_context_changed(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.thread_context_changed
        async def handle_thread_context_changed(context: AsyncBoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=thread_context_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_user_message(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.user_message
        async def handle_user_message(say: AsyncSay, set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            try:
                await set_status("is typing...")
                await say("Here you are!")
                listener_called.set()
            except Exception as e:
                await say(f"Oops, something went wrong (error: {e})")

        app.assistant(assistant)

        request = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_user_message_with_assistant_thread(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.user_message
        async def handle_user_message(say: AsyncSay, set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            try:
                await set_status("is typing...")
                await say("Here you are!")
                listener_called.set()
            except Exception as e:
                await say(f"Oops, something went wrong (error: {e})")

        app.assistant(assistant)

        request = AsyncBoltRequest(body=user_message_event_body_with_assistant_thread, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_message_changed(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.user_message
        async def handle_user_message():
            listener_called.set()

        @assistant.bot_message
        async def handle_bot_message():
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=user_message_event_body_with_action_token, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_target_called()

        request = AsyncBoltRequest(body=message_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await asyncio.sleep(0.1)
        assert not listener_called.is_set()

    @pytest.mark.asyncio
    async def test_channel_user_message_ignored(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.user_message
        async def handle_user_message():
            listener_called.set()

        @assistant.bot_message
        async def handle_bot_message():
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 404
        await asyncio.sleep(0.1)
        assert not listener_called.is_set()

    @pytest.mark.asyncio
    async def test_channel_message_changed_ignored(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.user_message
        async def handle_user_message():
            listener_called.set()

        @assistant.bot_message
        async def handle_bot_message():
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=channel_message_changed_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 404
        await asyncio.sleep(0.1)
        assert not listener_called.is_set()

    @pytest.mark.asyncio
    async def test_assistant_events_kwargs_disabled(self):
        app = AsyncApp(client=self.web_client, attaching_agent_kwargs_enabled=False)
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

    @pytest.mark.asyncio
    async def test_assistant_with_custom_listener_middleware(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()
        middleware_called = asyncio.Event()

        class TestAsyncMiddleware(AsyncMiddleware):
            async def async_process(
                self,
                *,
                req: AsyncBoltRequest,
                resp: BoltResponse,
                next: Callable[[], Awaitable[BoltResponse]],
            ) -> Optional[BoltResponse]:
                middleware_called.set()
                # Verify assistant utilities are available (set by _AsyncAssistantMiddleware before this)
                assert req.context.get("set_status") is not None
                assert req.context.get("set_title") is not None
                assert req.context.get("set_suggested_prompts") is not None
                assert req.context.get("get_thread_context") is not None
                assert req.context.get("save_thread_context") is not None
                return await next()

        @assistant.thread_started(middleware=[TestAsyncMiddleware()])
        async def start_thread(say: AsyncSay, set_suggested_prompts: AsyncSetSuggestedPrompts, context: AsyncBoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            await say("Hi, how can I help you today?")
            await set_suggested_prompts(
                prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}]
            )
            listener_called.set()

        @assistant.user_message(middleware=[TestAsyncMiddleware()])
        async def handle_user_message(say: AsyncSay, set_status: AsyncSetStatus, context: AsyncBoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            await set_status("is typing...")
            await say("Here you are!")
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True
        assert (await asyncio.wait_for(middleware_called.wait(), timeout=0.1)) is True

        listener_called.clear()
        middleware_called.clear()

        request = AsyncBoltRequest(body=user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True
        assert (await asyncio.wait_for(middleware_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_assistant_custom_middleware_can_short_circuit(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        class BlockingAsyncMiddleware(AsyncMiddleware):
            async def async_process(
                self,
                *,
                req: AsyncBoltRequest,
                resp: BoltResponse,
                next: Callable[[], Awaitable[BoltResponse]],
            ) -> Optional[BoltResponse]:
                # Intentionally not calling next() to short-circuit
                return BoltResponse(status=200)

        @assistant.thread_started(middleware=[BlockingAsyncMiddleware()])
        async def start_thread(say: AsyncSay, context: AsyncBoltContext):
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        await asyncio.sleep(0.1)
        assert not listener_called.is_set()


def build_payload(event: dict) -> dict:
    return {
        "token": "verification_token",
        "team_id": "T111",
        "enterprise_id": "E111",
        "api_app_id": "A111",
        "event": event,
        "type": "event_callback",
        "event_id": "Ev111",
        "event_time": 1599616881,
        "authorizations": [
            {
                "enterprise_id": "E111",
                "team_id": "T111",
                "user_id": "W111",
                "is_bot": True,
                "is_enterprise_install": False,
            }
        ],
    }


thread_started_event_body = build_payload(
    {
        "type": "assistant_thread_started",
        "assistant_thread": {
            "user_id": "W222",
            "context": {"channel_id": "C222", "team_id": "T111", "enterprise_id": "E111"},
            "channel_id": "D111",
            "thread_ts": "1726133698.626339",
        },
        "event_ts": "1726133698.665188",
    }
)

thread_context_changed_event_body = build_payload(
    {
        "type": "assistant_thread_context_changed",
        "assistant_thread": {
            "user_id": "W222",
            "context": {"channel_id": "C333", "team_id": "T111", "enterprise_id": "E111"},
            "channel_id": "D111",
            "thread_ts": "1726133698.626339",
        },
        "event_ts": "1726133698.665188",
    }
)


user_message_event_body = build_payload(
    {
        "user": "W222",
        "type": "message",
        "ts": "1726133700.887259",
        "text": "When Slack was released?",
        "team": "T111",
        "user_team": "T111",
        "source_team": "T222",
        "user_profile": {},
        "thread_ts": "1726133698.626339",
        "parent_user_id": "W222",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
    }
)


user_message_event_body_with_assistant_thread = build_payload(
    {
        "user": "W222",
        "type": "message",
        "ts": "1726133700.887259",
        "text": "When Slack was released?",
        "team": "T111",
        "user_team": "T111",
        "source_team": "T222",
        "user_profile": {},
        "thread_ts": "1726133698.626339",
        "parent_user_id": "W222",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
        "assistant_thread": {"XXX": "YYY"},
    }
)


user_message_event_body_with_action_token = build_payload(
    {
        "user": "W222",
        "type": "message",
        "ts": "1726133700.887259",
        "text": "When Slack was released?",
        "team": "T111",
        "user_team": "T111",
        "source_team": "T222",
        "user_profile": {},
        "thread_ts": "1726133698.626339",
        "parent_user_id": "W222",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
        "assistant_thread": {"action_token": "10647138185092.960436384805.afce3599"},
    }
)

message_changed_event_body = build_payload(
    {
        "type": "message",
        "subtype": "message_changed",
        "message": {
            "text": "New chat",
            "subtype": "assistant_app_thread",
            "user": "U222",
            "type": "message",
            "edited": {},
            "thread_ts": "1726133698.626339",
            "reply_count": 2,
            "reply_users_count": 2,
            "latest_reply": "1726133700.887259",
            "reply_users": ["U222", "W111"],
            "is_locked": False,
            "assistant_app_thread": {"title": "When Slack was released?", "title_blocks": [], "artifacts": []},
            "ts": "1726133698.626339",
        },
        "previous_message": {
            "text": "New chat",
            "subtype": "assistant_app_thread",
            "user": "U222",
            "type": "message",
            "edited": {},
            "thread_ts": "1726133698.626339",
            "reply_count": 2,
            "reply_users_count": 2,
            "latest_reply": "1726133700.887259",
            "reply_users": ["U222", "W111"],
            "is_locked": False,
        },
        "channel": "D111",
        "hidden": True,
        "ts": "1726133701.028300",
        "event_ts": "1726133701.028300",
        "channel_type": "im",
    }
)

channel_user_message_event_body = build_payload(
    {
        "user": "W222",
        "type": "message",
        "ts": "1726133700.887259",
        "text": "When Slack was released?",
        "team": "T111",
        "user_team": "T111",
        "source_team": "T222",
        "user_profile": {},
        "thread_ts": "1726133698.626339",
        "parent_user_id": "W222",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "channel",
    }
)

channel_message_changed_event_body = build_payload(
    {
        "type": "message",
        "subtype": "message_changed",
        "message": {
            "text": "New chat",
            "user": "U222",
            "type": "message",
            "edited": {},
            "thread_ts": "1726133698.626339",
            "reply_count": 2,
            "reply_users_count": 2,
            "latest_reply": "1726133700.887259",
            "reply_users": ["U222", "W111"],
            "is_locked": False,
            "ts": "1726133698.626339",
        },
        "previous_message": {
            "text": "New chat",
            "user": "U222",
            "type": "message",
            "edited": {},
            "thread_ts": "1726133698.626339",
            "reply_count": 2,
            "reply_users_count": 2,
            "latest_reply": "1726133700.887259",
            "reply_users": ["U222", "W111"],
            "is_locked": False,
        },
        "channel": "D111",
        "hidden": True,
        "ts": "1726133701.028300",
        "event_ts": "1726133701.028300",
        "channel_type": "channel",
    }
)
