import asyncio
import json
from urllib.parse import quote

import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.async_app import AsyncApp, AsyncAssistant, AsyncBoltContext, AsyncBoltRequest, AsyncSayStream
from tests.mock_web_api_server import cleanup_mock_web_api_server_async, setup_mock_web_api_server_async
from tests.scenario_tests_async.test_app import app_mention_event_body
from tests.scenario_tests_async.test_events_assistant import thread_started_event_body
from tests.scenario_tests_async.test_events_assistant import user_message_event_body as threaded_user_message_event_body
from tests.scenario_tests_async.test_message_bot import bot_message_event_payload, user_message_event_payload
from tests.scenario_tests_async.test_view_submission import body as view_submission_body
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncEventsSayStream:
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
    async def test_say_stream_injected_for_app_mention(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

        @app.event("app_mention")
        async def handle_mention(say_stream: AsyncSayStream, context: AsyncBoltContext):
            assert say_stream is not None
            assert isinstance(say_stream, AsyncSayStream)
            assert say_stream == context.say_stream
            assert say_stream.channel == "C111"
            assert say_stream.thread_ts == "1595926230.009600"
            assert say_stream.recipient_team_id == context.team_id
            assert say_stream.recipient_user_id == context.user_id
            listener_called.set()

        request = AsyncBoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_say_stream_with_org_level_install(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

        @app.event("app_mention")
        async def handle_mention(say_stream: AsyncSayStream, context: AsyncBoltContext):
            assert context.team_id is None
            assert context.enterprise_id == "E111"
            assert say_stream is not None
            assert isinstance(say_stream, AsyncSayStream)
            assert say_stream.recipient_team_id == "E111"
            listener_called.set()

        request = AsyncBoltRequest(body=org_app_mention_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_say_stream_injected_for_threaded_message(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

        @app.event("message")
        async def handle_message(say_stream: AsyncSayStream, context: AsyncBoltContext):
            assert say_stream is not None
            assert isinstance(say_stream, AsyncSayStream)
            assert say_stream == context.say_stream
            assert say_stream.channel == "D111"
            assert say_stream.thread_ts == "1726133698.626339"
            assert say_stream.recipient_team_id == context.team_id
            assert say_stream.recipient_user_id == context.user_id
            listener_called.set()

        request = AsyncBoltRequest(body=threaded_user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_say_stream_in_user_message(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

        @app.message("")
        async def handle_user_message(say_stream: AsyncSayStream, context: AsyncBoltContext):
            assert say_stream is not None
            assert isinstance(say_stream, AsyncSayStream)
            assert say_stream == context.say_stream
            assert say_stream.channel == "C111"
            assert say_stream.thread_ts == "1610261659.001400"
            assert say_stream.recipient_team_id == context.team_id
            assert say_stream.recipient_user_id == context.user_id
            listener_called.set()

        request = AsyncBoltRequest(body=user_message_event_payload, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_say_stream_in_bot_message(self):
        app = AsyncApp(client=self.web_client)
        listener_called = asyncio.Event()

        @app.message("")
        async def handle_user_message(say_stream: AsyncSayStream, context: AsyncBoltContext):
            assert say_stream is not None
            assert isinstance(say_stream, AsyncSayStream)
            assert say_stream == context.say_stream
            assert say_stream.channel == "C111"
            assert say_stream.thread_ts == "1610261539.000900"
            assert say_stream.recipient_team_id == context.team_id
            assert say_stream.recipient_user_id == context.user_id
            listener_called.set()

        request = AsyncBoltRequest(body=bot_message_event_payload, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_say_stream_in_assistant_thread_started(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.thread_started
        async def start_thread(say_stream: AsyncSayStream, context: AsyncBoltContext):
            assert say_stream is not None
            assert isinstance(say_stream, AsyncSayStream)
            assert say_stream == context.say_stream
            assert say_stream.channel == "D111"
            assert say_stream.thread_ts == "1726133698.626339"
            assert say_stream.recipient_team_id == context.team_id
            assert say_stream.recipient_user_id == context.user_id
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_say_stream_in_assistant_user_message(self):
        app = AsyncApp(client=self.web_client)
        assistant = AsyncAssistant()
        listener_called = asyncio.Event()

        @assistant.user_message
        async def handle_user_message(say_stream: AsyncSayStream, context: AsyncBoltContext):
            assert say_stream is not None
            assert isinstance(say_stream, AsyncSayStream)
            assert say_stream == context.say_stream
            assert say_stream.channel == "D111"
            assert say_stream.thread_ts == "1726133698.626339"
            assert say_stream.recipient_team_id == context.team_id
            assert say_stream.recipient_user_id == context.user_id
            listener_called.set()

        app.assistant(assistant)

        request = AsyncBoltRequest(body=threaded_user_message_event_body, mode="socket_mode")
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True

    @pytest.mark.asyncio
    async def test_say_stream_is_none_for_view_submission(self):
        app = AsyncApp(client=self.web_client, request_verification_enabled=False)
        listener_called = asyncio.Event()

        @app.view("view-id")
        async def handle_view(ack, say_stream, context: AsyncBoltContext):
            await ack()
            assert say_stream is None
            assert context.say_stream is None
            listener_called.set()

        request = AsyncBoltRequest(
            body=f"payload={quote(json.dumps(view_submission_body))}",
        )
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert (await asyncio.wait_for(listener_called.wait(), timeout=0.1)) is True


org_app_mention_event_body = {
    "token": "verification_token",
    "team_id": "T111",
    "enterprise_id": "E111",
    "api_app_id": "A111",
    "event": {
        "client_msg_id": "9cbd4c5b-7ddf-4ede-b479-ad21fca66d63",
        "type": "app_mention",
        "text": "<@W111> Hi there!",
        "user": "W222",
        "ts": "1595926230.009600",
        "team": "T111",
        "channel": "C111",
        "event_ts": "1595926230.009600",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1595926230,
    "authorizations": [
        {
            "enterprise_id": "E111",
            "team_id": None,
            "user_id": "W111",
            "is_bot": True,
            "is_enterprise_install": True,
        }
    ],
    "is_ext_shared_channel": False,
}
