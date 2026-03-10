import asyncio

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.context.set_status.async_set_status import AsyncSetStatus
from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from slack_bolt.context.set_title.async_set_title import AsyncSetTitle
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server_async,
    setup_mock_web_api_server_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


# TODO: VALIDATE THIS AI SLOP IS CORRECT
def build_event_body(event: dict) -> dict:
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


top_level_message_body = build_event_body(
    {
        "type": "message",
        "user": "W222",
        "text": "hello",
        "ts": "1234567890.123456",
        "channel": "C111",
        "event_ts": "1234567890.123456",
    }
)

threaded_message_body = build_event_body(
    {
        "type": "message",
        "user": "W222",
        "text": "hello in thread",
        "ts": "1234567890.999999",
        "thread_ts": "1234567890.123456",
        "channel": "C111",
        "event_ts": "1234567890.999999",
    }
)

app_mention_body = build_event_body(
    {
        "type": "app_mention",
        "user": "W222",
        "text": "<@W111> hello",
        "ts": "1234567890.123456",
        "channel": "C111",
        "event_ts": "1234567890.123456",
    }
)

no_channel_event_body = build_event_body(
    {
        "type": "team_join",
        "user": {"id": "W222"},
    }
)


class TestAsyncAttachingAgentKwargs:
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

    async def _wait_for(self, state, key="called", timeout=2.0):
        count = 0
        while state[key] is False and count < timeout / 0.1:
            await asyncio.sleep(0.1)
            count += 1
        assert state[key] is True

    @pytest.mark.asyncio
    async def test_top_level_message_uses_ts(self):
        app = AsyncApp(client=self.web_client)
        state = {"called": False}

        @app.event("message")
        async def handle(context):
            assert isinstance(context["set_status"], AsyncSetStatus)
            assert isinstance(context["set_title"], AsyncSetTitle)
            assert isinstance(context["set_suggested_prompts"], AsyncSetSuggestedPrompts)
            assert context["set_status"].thread_ts == "1234567890.123456"
            state["called"] = True

        response = await app.async_dispatch(AsyncBoltRequest(body=top_level_message_body, mode="socket_mode"))
        assert response.status == 200
        await self._wait_for(state)

    @pytest.mark.asyncio
    async def test_threaded_message_uses_thread_ts(self):
        app = AsyncApp(client=self.web_client)
        state = {"called": False}

        @app.event("message")
        async def handle(context):
            assert isinstance(context["set_status"], AsyncSetStatus)
            assert context["set_status"].thread_ts == "1234567890.123456"
            state["called"] = True

        response = await app.async_dispatch(AsyncBoltRequest(body=threaded_message_body, mode="socket_mode"))
        assert response.status == 200
        await self._wait_for(state)

    @pytest.mark.asyncio
    async def test_app_mention_event(self):
        app = AsyncApp(client=self.web_client)
        state = {"called": False}

        @app.event("app_mention")
        async def handle(context):
            assert isinstance(context["set_status"], AsyncSetStatus)
            assert isinstance(context["set_title"], AsyncSetTitle)
            assert isinstance(context["set_suggested_prompts"], AsyncSetSuggestedPrompts)
            assert context["set_status"].thread_ts == "1234567890.123456"
            state["called"] = True

        response = await app.async_dispatch(AsyncBoltRequest(body=app_mention_body, mode="socket_mode"))
        assert response.status == 200
        await self._wait_for(state)

    @pytest.mark.asyncio
    async def test_message_listener_top_level(self):
        app = AsyncApp(client=self.web_client)
        state = {"called": False}

        @app.message("hello")
        async def handle(context):
            assert isinstance(context["set_status"], AsyncSetStatus)
            assert context["set_status"].thread_ts == "1234567890.123456"
            state["called"] = True

        response = await app.async_dispatch(AsyncBoltRequest(body=top_level_message_body, mode="socket_mode"))
        assert response.status == 200
        await self._wait_for(state)

    @pytest.mark.asyncio
    async def test_no_channel_id_skips_gracefully(self):
        app = AsyncApp(client=self.web_client)
        state = {"called": False}

        @app.event("team_join")
        async def handle(context):
            assert "set_status" not in context
            assert "set_title" not in context
            assert "set_suggested_prompts" not in context
            state["called"] = True

        response = await app.async_dispatch(AsyncBoltRequest(body=no_channel_event_body, mode="socket_mode"))
        assert response.status == 200
        await self._wait_for(state)

    @pytest.mark.asyncio
    async def test_opt_out(self):
        app = AsyncApp(client=self.web_client, attaching_agent_kwargs_enabled=False)
        state = {"called": False}

        @app.event("message")
        async def handle(context):
            assert "set_status" not in context
            assert "set_title" not in context
            assert "set_suggested_prompts" not in context
            state["called"] = True

        response = await app.async_dispatch(AsyncBoltRequest(body=top_level_message_body, mode="socket_mode"))
        assert response.status == 200
        await self._wait_for(state)
