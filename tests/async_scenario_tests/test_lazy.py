import asyncio
import json
from time import time
from urllib.parse import quote

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncLazy:
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

    # ----------------
    #  utilities
    # ----------------

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body, timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_valid_request(self) -> AsyncBoltRequest:
        payload = {
            "type": "block_actions",
            "user": {"id": "W111",},
            "api_app_id": "A111",
            "token": "verification_token",
            "trigger_id": "111.222.valid",
            "team": {"id": "T111",},
            "channel": {"id": "C111", "name": "test-channel"},
            "response_url": "https://hooks.slack.com/actions/T111/111/random-value",
            "actions": [
                {
                    "action_id": "a",
                    "block_id": "b",
                    "text": {"type": "plain_text", "text": "Button"},
                    "value": "click_me_123",
                    "type": "button",
                    "action_ts": "1596530385.194939",
                }
            ],
        }
        raw_body = f"payload={quote(json.dumps(payload))}"
        timestamp = str(int(time()))
        return AsyncBoltRequest(
            body=raw_body, headers=self.build_headers(timestamp, raw_body)
        )

    # ----------------
    #  tests
    # ----------------

    @pytest.mark.asyncio
    async def test_lazy(self):
        async def just_ack(ack):
            await ack()

        async def async1(say):
            await asyncio.sleep(0.3)
            await say(text="lazy function 1")

        async def async2(say):
            await asyncio.sleep(0.5)
            await say(text="lazy function 2")

        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret,)
        app.action("a")(
            ack=just_ack, lazy=[async1, async2],
        )

        request = self.build_valid_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        await asyncio.sleep(1)  # wait a bit
        assert self.mock_received_requests["/chat.postMessage"] == 2
