import asyncio
import re

import pytest
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow
from slack_bolt.request.async_request import AsyncBoltRequest
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server,
    setup_mock_web_api_server,
)


class TestAsyncOAuthFlow:
    mock_api_server_base_url = "http://localhost:8888"

    @pytest.fixture
    def event_loop(self):
        setup_mock_web_api_server(self)
        loop = asyncio.get_event_loop()
        yield loop
        loop.close()
        cleanup_mock_web_api_server(self)

    def next(self):
        pass

    @pytest.mark.asyncio
    async def test_instantiation(self):
        oauth_flow = AsyncOAuthFlow(
            client_id="111.222",
            client_secret="xxx",
            scopes=["chat:write", "commands"],
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
        )
        assert oauth_flow is not None

    @pytest.mark.asyncio
    async def test_handle_installation(self):
        oauth_flow = AsyncOAuthFlow(
            client_id="111.222",
            client_secret="xxx",
            scopes=["chat:write", "commands"],
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
        )
        req = AsyncBoltRequest(body="")
        resp = await oauth_flow.handle_installation(req)
        assert resp.status == 302
        url = resp.headers["location"][0]
        assert (
            re.compile(
                "https://slack.com/oauth/v2/authorize\\?state=[-0-9a-z]+."
                "&client_id=111\\.222"
                "&scope=chat:write,commands"
                "&user_scope="
            ).match(url)
            is not None
        )

    @pytest.mark.asyncio
    async def test_handle_callback(self):
        oauth_flow = AsyncOAuthFlow(
            client=AsyncWebClient(base_url=self.mock_api_server_base_url),
            client_id="111.222",
            client_secret="xxx",
            scopes=["chat:write", "commands"],
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
            success_url="https://www.example.com/completion",
            failure_url="https://www.example.com/failure",
        )
        state = await oauth_flow.issue_new_state(None)
        req = AsyncBoltRequest(
            body="",
            query=f"code=foo&state={state}",
            headers={"cookie": [f"{oauth_flow.oauth_state_cookie_name}={state}"]},
        )
        resp = await oauth_flow.handle_callback(req)
        assert resp.status == 200
        assert "https://www.example.com/completion" in resp.body

    @pytest.mark.asyncio
    async def test_handle_callback_invalid_state(self):
        oauth_flow = AsyncOAuthFlow(
            client_id="111.222",
            client_secret="xxx",
            scopes=["chat:write", "commands"],
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
        )
        state = await oauth_flow.issue_new_state(None)
        req = AsyncBoltRequest(
            body="",
            query=f"code=foo&state=invalid",
            headers={"cookie": [f"{oauth_flow.oauth_state_cookie_name}={state}"]},
        )
        resp = await oauth_flow.handle_callback(req)
        assert resp.status == 400
