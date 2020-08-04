import asyncio
import json
import re
from time import time

import pytest

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncMessage:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = AsyncWebClient(token=valid_token, base_url=mock_api_server_base_url,)

    @pytest.fixture
    def event_loop(self):
        old_os_env = remove_os_env_temporarily()
        try:
            setup_mock_web_api_server(self)
            loop = asyncio.get_event_loop()
            yield loop
            loop.close()
            cleanup_mock_web_api_server(self)
        finally:
            restore_os_env(old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body, timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_request(self) -> AsyncBoltRequest:
        timestamp, body = str(int(time())), json.dumps(message_payload)
        return AsyncBoltRequest(body=body, headers=self.build_headers(timestamp, body))

    @pytest.mark.asyncio
    async def test_string_keyword(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret,)
        app.message("Hello")(whats_up)

        request = self.build_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1
        await asyncio.sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1

    @pytest.mark.asyncio
    async def test_string_keyword_unmatched(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret,)
        app.message("HELLO")(whats_up)

        request = self.build_request()
        response = await app.async_dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    @pytest.mark.asyncio
    async def test_regexp_keyword(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret,)
        app.message(re.compile("He.lo"))(whats_up)

        request = self.build_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1
        await asyncio.sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1

    @pytest.mark.asyncio
    async def test_regexp_keyword_unmatched(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret,)
        app.message(re.compile("HELLO"))(whats_up)

        request = self.build_request()
        response = await app.async_dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1


message_payload = {
    "token": "verification_token",
    "team_id": "T111",
    "enterprise_id": "E111",
    "api_app_id": "A111",
    "event": {
        "client_msg_id": "a8744611-0210-4f85-9f15-5faf7fb225c8",
        "type": "message",
        "text": "Hello World!",
        "user": "W111",
        "ts": "1596183880.004200",
        "team": "T111",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "ezJ",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [{"type": "text", "text": "Hello World!"}],
                    }
                ],
            }
        ],
        "channel": "C111",
        "event_ts": "1596183880.004200",
        "channel_type": "channel",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1596183880,
    "authed_users": ["W111"],
}


async def whats_up(payload, say):
    assert payload == message_payload
    await say("What's up?")
