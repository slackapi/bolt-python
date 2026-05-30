import asyncio

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.async_app import AsyncApp, AsyncAssistant, AsyncBoltRequest
from slack_bolt.authorization import AuthorizeResult
from slack_bolt.context.assistant import async_assistant_utilities
from slack_bolt.context.assistant.thread_context import AssistantThreadContext
from slack_bolt.context.assistant.thread_context_store.async_store import AsyncAssistantThreadContextStore
from tests.scenario_tests_async.test_events_assistant import user_message_event_body


class RecordingDefaultAsyncAssistantThreadContextStore(AsyncAssistantThreadContextStore):
    def __init__(self, context, seen_bot_user_ids):
        self.seen_bot_user_ids = seen_bot_user_ids
        self.seen_bot_user_ids.append(context.bot_user_id)

    async def find(self, *, channel_id: str, thread_ts: str):
        return AssistantThreadContext({"channel_id": "C222", "team_id": "T111"})

    async def save(self, *, channel_id: str, thread_ts: str, context):
        pass


class TestAsyncAppAssistant:
    @pytest.mark.asyncio
    async def test_user_message_get_thread_context_store_is_initialized_after_authorize(self, monkeypatch):
        seen_bot_user_ids = []

        def build_store(context):
            return RecordingDefaultAsyncAssistantThreadContextStore(context, seen_bot_user_ids)

        monkeypatch.setattr(
            async_assistant_utilities,
            "DefaultAsyncAssistantThreadContextStore",
            build_store,
        )

        async def authorize(context, enterprise_id, team_id, user_id):
            return AuthorizeResult(
                enterprise_id=enterprise_id,
                team_id=team_id,
                bot_user_id="W23456789",
                bot_id="B111",
                bot_token="xoxb-valid",
            )

        app = AsyncApp(
            client=AsyncWebClient(token=None),
            authorize=authorize,
            process_before_response=True,
        )
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.user_message
        async def handle_user_message(get_thread_context):
            assert await get_thread_context() == {"channel_id": "C222", "team_id": "T111"}
            listener_called.set()

        app.assistant(assistant)

        response = await app.async_dispatch(AsyncBoltRequest(body=user_message_event_body, mode="socket_mode"))

        assert response.status == 200
        assert listener_called.is_set()
        assert seen_bot_user_ids == ["W23456789"]
