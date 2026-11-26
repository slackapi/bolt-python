from time import time

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import cleanup_mock_web_api_server_async, setup_mock_web_api_server_async
from tests.scenario_tests import test_slash_command
from tests.scenario_tests.test_request_parsing import malformed_unsigned_bodies, plain_values, signed_bodies
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncRequestParsing:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = AsyncWebClient(token=valid_token, base_url=mock_api_server_base_url)

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server_async(self)
        try:
            yield
        finally:
            cleanup_mock_web_api_server_async(self)
            restore_os_env(old_os_env)

    def build_request(self, body: str, defer_parsing: bool) -> AsyncBoltRequest:
        timestamp = str(int(time()))
        content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
        return AsyncBoltRequest(
            body=body,
            headers={
                "content-type": [content_type],
                "x-slack-signature": [self.signature_verifier.generate_signature(body=body, timestamp=timestamp)],
                "x-slack-request-timestamp": [timestamp],
            },
            defer_parsing=defer_parsing,
        )

    async def capture_after_dispatch(self, request: AsyncBoltRequest) -> dict:
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)
        captured = {}

        @app.middleware
        async def capture(context, body, next):
            captured["context"] = plain_values(context)
            captured["body"] = body
            captured["client_default_params"] = dict(context.client.default_params)
            await next()

        await app.async_dispatch(request)
        return captured

    @pytest.mark.asyncio
    async def test_deferred_parsing_matches_eager_parsing(self):
        for body in signed_bodies:
            eager = await self.capture_after_dispatch(self.build_request(body, defer_parsing=False))
            deferred = await self.capture_after_dispatch(self.build_request(body, defer_parsing=True))
            assert eager != {}
            assert deferred == eager, body

    @pytest.mark.asyncio
    async def test_malformed_unsigned_deferred_requests_are_rejected(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)
        for body in malformed_unsigned_bodies:
            request = AsyncBoltRequest(body=body, headers={"content-type": ["application/json"]}, defer_parsing=True)
            assert (await app.async_dispatch(request)).status == 401

    @pytest.mark.asyncio
    async def test_context_set_after_creation_wins_over_body(self):
        request = self.build_request(test_slash_command.slash_command_body, defer_parsing=True)
        request.context["team_id"] = "T_FROM_ADAPTER"
        request.complete_deferred_parsing()
        assert request.context.team_id == "T_FROM_ADAPTER"
        assert request.context.user_id == "W111"

    @pytest.mark.asyncio
    async def test_deferred_parsing_without_request_verification(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret, request_verification_enabled=False)
        captured = {}

        @app.middleware
        async def capture(context, next):
            captured["team_id"] = context.team_id
            await next()

        await app.async_dispatch(AsyncBoltRequest(body=test_slash_command.slash_command_body, defer_parsing=True))
        assert captured["team_id"] == "T111"

    @pytest.mark.asyncio
    async def test_signed_invalid_json_is_handled_by_the_error_handler(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)
        response = await app.async_dispatch(self.build_request('{"type": "event_callback", ', defer_parsing=True))
        assert response.status == 500

    @pytest.mark.asyncio
    async def test_ssl_check_on_deferred_request(self):
        app = AsyncApp(client=self.web_client, signing_secret=self.signing_secret)
        response = await app.async_dispatch(AsyncBoltRequest(body="token=random&ssl_check=1", defer_parsing=True))
        assert response.status == 200
