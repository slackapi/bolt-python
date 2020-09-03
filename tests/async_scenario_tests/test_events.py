import asyncio
import json
from random import random
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


class TestAsyncEvents:
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

    def build_valid_app_mention_request(self) -> AsyncBoltRequest:
        timestamp, body = str(int(time())), json.dumps(app_mention_payload)
        return AsyncBoltRequest(body=body, headers=self.build_headers(timestamp, body))

    @pytest.mark.asyncio
    async def test_mock_server_is_running(self):
        resp = await self.web_client.api_test()
        assert resp != None

    @pytest.mark.asyncio
    async def test_app_mention(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret,)
        app.event("app_mention")(whats_up)

        request = self.build_valid_app_mention_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1
        await asyncio.sleep(1)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1

    @pytest.mark.asyncio
    async def test_process_before_response(self):
        app = AsyncApp(
            client=self.web_client,
            signing_secret=self.signing_secret,
            process_before_response=True,
        )
        app.event("app_mention")(whats_up)

        request = self.build_valid_app_mention_request()
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1
        # no sleep here
        assert self.mock_received_requests["/chat.postMessage"] == 1

    @pytest.mark.asyncio
    async def test_middleware_skip(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)
        app.event("app_mention", middleware=[skip_middleware])(whats_up)

        request = self.build_valid_app_mention_request()
        response = await app.async_dispatch(request)
        assert response.status == 404
        assert self.mock_received_requests["/auth.test"] == 1

    @pytest.mark.asyncio
    async def test_simultaneous_requests(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret,)
        app.event("app_mention")(random_sleeper)

        request = self.build_valid_app_mention_request()

        times = 10
        tasks = []
        for i in range(times):
            tasks.append(asyncio.ensure_future(app.async_dispatch(request)))

        await asyncio.sleep(5)
        # Verifies all the tasks have been completed with 200 OK
        assert sum([t.result().status for t in tasks if t.done()]) == 200 * times

        assert self.mock_received_requests["/auth.test"] == times
        assert self.mock_received_requests["/chat.postMessage"] == times


app_mention_payload = {
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
    "authed_users": ["W111"],
}


async def random_sleeper(payload, say, event):
    assert payload == app_mention_payload
    assert payload["event"] == event
    seconds = random() + 2  # 2-3 seconds
    await asyncio.sleep(seconds)
    await say(f"Sending this message after sleeping for {seconds} seconds")


async def whats_up(payload, say, event):
    assert payload == app_mention_payload
    assert payload["event"] == event
    await say("What's up?")


async def skip_middleware(req, resp, next):
    # return next()
    pass
