import asyncio
import json
from time import time
from urllib.parse import quote

import pytest

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request import AsyncBoltRequest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient
from tests.mock_web_api_server import \
    setup_mock_web_api_server, cleanup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncShortcut():
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
            setup_mock_web_api_server(self)
            loop = asyncio.get_event_loop()
            yield loop
            loop.close()
            cleanup_mock_web_api_server(self)
        finally:
            restore_os_env(old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp]
        }

    def build_valid_request(self) -> AsyncBoltRequest:
        timestamp = str(int(time()))
        return AsyncBoltRequest(body=raw_body, headers=self.build_headers(timestamp, raw_body))

    @pytest.mark.asyncio
    async def test_mock_server_is_running(self):
        resp = await self.web_client.api_test()
        assert resp != None

    @pytest.mark.asyncio
    async def test_success(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.shortcut("test-shortcut")(simple_listener)

        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1

    @pytest.mark.asyncio
    async def test_process_before_response(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
            process_before_response=True,
        )
        app.shortcut("test-shortcut")(simple_listener)

        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1

    @pytest.mark.asyncio
    async def test_failure(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

        app.shortcut("another-one")(simple_listener)
        response = await app.async_dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 2


payload = {
    "type": "shortcut",
    "token": "verification_token",
    "action_ts": "111.111",
    "team": {
        "id": "T111",
        "domain": "workspace-domain",
        "enterprise_id": "E111",
        "enterprise_name": "Org Name"
    },
    "user": {
        "id": "W111",
        "username": "primary-owner",
        "team_id": "T111"
    },
    "callback_id": "test-shortcut",
    "trigger_id": "111.111.xxxxxx"
}

raw_body = f"payload={quote(json.dumps(payload))}"


async def simple_listener(ack):
    await ack()
