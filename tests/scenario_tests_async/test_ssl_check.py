from time import time

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server_async,
    setup_mock_web_api_server_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncSSLCheck:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
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

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    @pytest.mark.asyncio
    async def test_mock_server_is_running(self):
        resp = await self.web_client.api_test()
        assert resp != None

    @pytest.mark.asyncio
    async def test_ssl_check(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)

        timestamp, body = str(int(time())), "token=random&ssl_check=1"
        request: AsyncBoltRequest = AsyncBoltRequest(
            body=body,
            query={},
            headers={
                "content-type": ["application/x-www-form-urlencoded"],
                "x-slack-signature": [self.generate_signature(body, timestamp)],
                "x-slack-request-timestamp": [timestamp],
            },
        )
        response = await app.async_dispatch(request)
        assert response.status == 200
        assert response.body == ""
