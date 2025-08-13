import asyncio
import json
import time

import pytest
from unittest.mock import Mock, MagicMock
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import (
    assert_received_request_count_async,
    setup_mock_web_api_server_async,
    cleanup_mock_web_api_server_async,
    assert_auth_test_count_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env

async def fake_sleep(seconds):
    pass

class TestAsyncFunction:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = AsyncWebClient(
        token=valid_token,
        base_url=mock_api_server_base_url,
    )

    @pytest.fixture
    def event_loop(self):
        old_os_env = remove_os_env_temporarily()
        try:
            setup_mock_web_api_server_async(self)
            loop = asyncio.get_event_loop()
            yield loop
            loop.close()
            cleanup_mock_web_api_server_async(self)
        finally:
            restore_os_env(old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_request_from_body(self, message_body: dict) -> AsyncBoltRequest:
        timestamp, body = str(int(time.time())), json.dumps(message_body)
        return AsyncBoltRequest(body=body, headers=self.build_headers(timestamp, body))

    def setup_time_mocks(self, *, monkeypatch: pytest.MonkeyPatch, time_mock: Mock, sleep_mock: MagicMock):
        monkeypatch.setattr(time, "time", time_mock)
        monkeypatch.setattr(asyncio, "sleep", sleep_mock)

    @pytest.mark.asyncio
    async def test_mock_server_is_running(self):
        resp = await self.web_client.api_test()
        assert resp is not None

    @pytest.mark.asyncio
    async def test_valid_callback_id_success(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(reverse)

        request = self.build_request_from_body(function_body)
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, "/functions.completeSuccess", 1)

    @pytest.mark.asyncio
    async def test_valid_callback_id_complete(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(complete_it)

        request = self.build_request_from_body(function_body)
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, "/functions.completeSuccess", 1)

    @pytest.mark.asyncio
    async def test_valid_callback_id_error(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(reverse_error)

        request = self.build_request_from_body(function_body)
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)
        await assert_received_request_count_async(self, "/functions.completeError", 1)

    @pytest.mark.asyncio
    async def test_invalid_callback_id(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse")(reverse)

        request = self.build_request_from_body(wrong_id_function_body)
        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_auto_acknowledge_false_with_acknowledging(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse", auto_acknowledge=False)(just_ack)

        request = self.build_request_from_body(function_body)
        response = await app.async_dispatch(request)
        assert response.status == 200
        await assert_auth_test_count_async(self, 1)

    @pytest.mark.asyncio
    async def test_auto_acknowledge_false_without_acknowledging(self, caplog, monkeypatch):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse", auto_acknowledge=False)(just_no_ack)
        request = self.build_request_from_body(function_body)
        
        self.setup_time_mocks(
            monkeypatch=monkeypatch,
            time_mock=Mock(side_effect=[current_time for current_time in range(100)]),
            sleep_mock=MagicMock(side_effect=fake_sleep),
        )

        response = await app.async_dispatch(request)
        assert response.status == 404
        await assert_auth_test_count_async(self, 1)
        assert f"WARNING {just_no_ack.__name__} didn't call ack()" in caplog.text

    @pytest.mark.asyncio
    async def test_function_handler_timeout(self, monkeypatch):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.function("reverse", auto_acknowledge=False)(just_no_ack)
        request = self.build_request_from_body(function_body)

        sleep_mock = MagicMock(side_effect=fake_sleep)
        self.setup_time_mocks(
            monkeypatch=monkeypatch,
            time_mock=Mock(side_effect=[current_time for current_time in range(100)]),
            sleep_mock=sleep_mock,
        )

        response = await app.async_dispatch(request)

        assert response.status == 404
        await assert_auth_test_count_async(self, 1)
        assert (
            sleep_mock.call_count == 5
        ), f"Expected handler to time out after calling time.sleep 5 times, but it was called {sleep_mock.call_count} times"


function_body = {
    "token": "verification_token",
    "enterprise_id": "E111",
    "team_id": "T111",
    "api_app_id": "A111",
    "event": {
        "type": "function_executed",
        "function": {
            "id": "Fn111",
            "callback_id": "reverse",
            "title": "Reverse",
            "description": "Takes a string and reverses it",
            "type": "app",
            "input_parameters": [
                {
                    "type": "string",
                    "name": "stringToReverse",
                    "description": "The string to reverse",
                    "title": "String To Reverse",
                    "is_required": True,
                }
            ],
            "output_parameters": [
                {
                    "type": "string",
                    "name": "reverseString",
                    "description": "The string in reverse",
                    "title": "Reverse String",
                    "is_required": True,
                }
            ],
            "app_id": "A111",
            "date_updated": 1659054991,
        },
        "inputs": {"stringToReverse": "hello"},
        "function_execution_id": "Fx111",
        "event_ts": "1659055013.509853",
        "bot_access_token": "xwfp-valid",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1659055013,
    "authed_users": ["W111"],
}

wrong_id_function_body = {
    "token": "verification_token",
    "enterprise_id": "E111",
    "team_id": "T111",
    "api_app_id": "A111",
    "event": {
        "type": "function_executed",
        "function": {
            "id": "Fn111",
            "callback_id": "wrong_callback_id",
            "title": "Reverse",
            "description": "Takes a string and reverses it",
            "type": "app",
            "input_parameters": [
                {
                    "type": "string",
                    "name": "stringToReverse",
                    "description": "The string to reverse",
                    "title": "String To Reverse",
                    "is_required": True,
                }
            ],
            "output_parameters": [
                {
                    "type": "string",
                    "name": "reverseString",
                    "description": "The string in reverse",
                    "title": "Reverse String",
                    "is_required": True,
                }
            ],
            "app_id": "A111",
            "date_updated": 1659054991,
        },
        "inputs": {"stringToReverse": "hello"},
        "function_execution_id": "Fx111",
        "event_ts": "1659055013.509853",
        "bot_access_token": "xwfp-valid",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1659055013,
    "authed_users": ["W111"],
}


async def reverse(body, event, client, context, complete, inputs):
    assert body == function_body
    assert event == function_body["event"]
    assert inputs == function_body["event"]["inputs"]
    assert context.function_execution_id == "Fx111"
    assert complete.function_execution_id == "Fx111"
    assert context.function_bot_access_token == "xwfp-valid"
    assert context.client.token == "xwfp-valid"
    assert client.token == "xwfp-valid"
    assert complete.client.token == "xwfp-valid"
    await complete(
        outputs={"reverseString": "olleh"},
    )


async def reverse_error(body, event, fail):
    assert body == function_body
    assert event == function_body["event"]
    assert fail.function_execution_id == "Fx111"
    await fail(
        error="there was an error",
    )


async def complete_it(body, event, complete):
    assert body == function_body
    assert event == function_body["event"]
    await complete(
        outputs={},
    )


async def just_ack(ack, body, event):
    assert body == function_body
    assert event == function_body["event"]
    await ack()


async def just_no_ack(body, event):
    assert body == function_body
    assert event == function_body["event"]
