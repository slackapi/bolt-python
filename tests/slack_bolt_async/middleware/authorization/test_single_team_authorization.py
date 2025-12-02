import pytest
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.middleware.authorization.async_single_team_authorization import (
    AsyncSingleTeamAuthorization,
)
from slack_bolt.middleware.authorization.internals import _build_user_facing_authorize_error_message
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_bolt.response import BoltResponse
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server_async,
    setup_mock_web_api_server_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


async def next():
    return BoltResponse(status=200)


class TestSingleTeamAuthorization:

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server_async(self)
        try:
            self.mock_api_server_base_url = "http://localhost:8888"
            yield  # run the test here
        finally:
            cleanup_mock_web_api_server_async(self)
            restore_os_env(old_os_env)

    @pytest.mark.asyncio
    async def test_success_pattern(self):
        authorization = AsyncSingleTeamAuthorization()
        req = AsyncBoltRequest(body="payload={}", headers={})
        req.context["client"] = AsyncWebClient(base_url=self.mock_api_server_base_url, token="xoxb-valid")
        resp = BoltResponse(status=404)

        resp = await authorization.async_process(req=req, resp=resp, next=next)

        assert resp.status == 200
        assert resp.body == ""

    @pytest.mark.asyncio
    async def test_success_pattern_with_bot_scopes(self):
        client = AsyncWebClient(base_url=self.mock_api_server_base_url, token="xoxb-valid")
        authorization = AsyncSingleTeamAuthorization()
        req = AsyncBoltRequest(body="payload={}", headers={})
        req.context["client"] = client
        resp = BoltResponse(status=404)

        resp = await authorization.async_process(req=req, resp=resp, next=next)

        assert resp.status == 200
        assert resp.body == ""
        assert req.context.authorize_result.bot_scopes == ["chat:write", "commands"]
        assert req.context.authorize_result.user_scopes is None

    @pytest.mark.asyncio
    async def test_failure_pattern(self):
        authorization = AsyncSingleTeamAuthorization()
        req = AsyncBoltRequest(body="payload={}", headers={})
        req.context["client"] = AsyncWebClient(base_url=self.mock_api_server_base_url, token="dummy")
        resp = BoltResponse(status=404)

        resp = await authorization.async_process(req=req, resp=resp, next=next)

        assert resp.status == 200
        assert resp.body == _build_user_facing_authorize_error_message()

    @pytest.mark.asyncio
    async def test_failure_pattern_custom_message(self):
        authorization = AsyncSingleTeamAuthorization(user_facing_authorize_error_message="foo")
        req = AsyncBoltRequest(body="payload={}", headers={})
        req.context["client"] = AsyncWebClient(base_url=self.mock_api_server_base_url, token="dummy")
        resp = BoltResponse(status=404)

        resp = await authorization.async_process(req=req, resp=resp, next=next)

        assert resp.status == 200
        assert resp.body == "foo"
