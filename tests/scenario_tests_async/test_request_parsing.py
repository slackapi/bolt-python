import asyncio
import time

import pytest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.async_utils import async_parse_request
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

    def build_app(self, **kwargs) -> AsyncApp:
        return AsyncApp(client=self.web_client, signing_secret=self.signing_secret, **kwargs)

    def build_request(self, body: str) -> AsyncBoltRequest:
        timestamp = str(int(time.time()))
        content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
        return AsyncBoltRequest(
            body=body,
            headers={
                "content-type": [content_type],
                "x-slack-signature": [self.signature_verifier.generate_signature(body=body, timestamp=timestamp)],
                "x-slack-request-timestamp": [timestamp],
            },
        )

    async def capture_after_dispatch(self, request: AsyncBoltRequest) -> dict:
        app = self.build_app()
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
    async def test_dispatch_matches_parsing_before_dispatch(self):
        for body in signed_bodies:
            parsed_before = await self.capture_after_dispatch(await async_parse_request(self.build_request(body)))
            parsed_in_dispatch = await self.capture_after_dispatch(self.build_request(body))
            assert parsed_before != {}
            assert parsed_in_dispatch == parsed_before, body

    @pytest.mark.asyncio
    async def test_new_request_is_unparsed(self):
        request = self.build_request(test_slash_command.slash_command_body)
        assert request.body == {}
        assert request.context.team_id is None

    @pytest.mark.asyncio
    async def test_context_set_before_dispatch_wins_over_body(self):
        app = self.build_app()
        captured = {}

        @app.middleware
        async def capture(context, next):
            captured["team_id"] = context.team_id
            captured["user_id"] = context.user_id
            await next()

        request = self.build_request(test_slash_command.slash_command_body)
        request.context["team_id"] = "T_FROM_ADAPTER"
        await app.async_dispatch(request)
        assert captured == {"team_id": "T_FROM_ADAPTER", "user_id": "W111"}

    @pytest.mark.asyncio
    async def test_malformed_unsigned_requests_are_rejected(self):
        app = self.build_app()
        for body in malformed_unsigned_bodies:
            request = AsyncBoltRequest(body=body, headers={"content-type": ["application/json"]})
            assert (await app.async_dispatch(request)).status == 401

    @pytest.mark.asyncio
    async def test_parsing_without_request_verification(self):
        app = self.build_app(request_verification_enabled=False)
        captured = {}

        @app.middleware
        async def capture(context, next):
            captured["team_id"] = context.team_id
            await next()

        await app.async_dispatch(AsyncBoltRequest(body=test_slash_command.slash_command_body))
        assert captured["team_id"] == "T111"

    @pytest.mark.asyncio
    async def test_signed_invalid_json_is_handled_by_the_error_handler(self):
        response = await self.build_app().async_dispatch(self.build_request('{"type": "event_callback", '))
        assert response.status == 500

    @pytest.mark.asyncio
    async def test_ssl_check(self):
        response = await self.build_app().async_dispatch(AsyncBoltRequest(body="token=random&ssl_check=1"))
        assert response.status == 200

    @pytest.mark.asyncio
    async def test_to_copyable_keeps_the_parsed_body(self):
        request = await async_parse_request(self.build_request(test_slash_command.slash_command_body))
        copied = request.to_copyable()
        assert copied.body == request.body
        assert copied.body is not request.body
        assert copied.context.team_id == "T111"

    @pytest.mark.asyncio
    async def test_lazy_listener_reads_the_body(self):
        app = self.build_app()
        lazy_bodies = []

        async def just_ack(ack):
            await ack()

        async def read_body(body):
            lazy_bodies.append(body)

        app.command("/hello-world")(ack=just_ack, lazy=[read_body])
        response = await app.async_dispatch(self.build_request(test_slash_command.slash_command_body))
        assert response.status == 200
        deadline = time.time() + 2
        while not lazy_bodies and time.time() < deadline:
            await asyncio.sleep(0.05)
        assert lazy_bodies[0]["command"] == "/hello-world"
