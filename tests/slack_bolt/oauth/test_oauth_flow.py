import re

from slack_sdk import WebClient
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from slack_bolt import BoltRequest
from slack_bolt.oauth import OAuthFlow
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server,
    setup_mock_web_api_server,
)


class TestOAuthFlow:
    mock_api_server_base_url = "http://localhost:8888"

    def setup_method(self):
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def next(self):
        pass

    def test_instantiation(self):
        oauth_flow = OAuthFlow(
            client_id="111.222",
            client_secret="xxx",
            scopes=["chat:write", "commands"],
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
        )
        assert oauth_flow is not None

    def test_handle_installation(self):
        oauth_flow = OAuthFlow(
            client_id="111.222",
            client_secret="xxx",
            scopes=["chat:write", "commands"],
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
        )
        req = BoltRequest(body="")
        resp = oauth_flow.handle_installation(req)
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

    def test_handle_callback(self):
        oauth_flow = OAuthFlow(
            client=WebClient(base_url=self.mock_api_server_base_url),
            client_id="111.222",
            client_secret="xxx",
            scopes=["chat:write", "commands"],
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
            success_url="https://www.example.com/completion",
            failure_url="https://www.example.com/failure",
        )
        state = oauth_flow.issue_new_state(None)
        req = BoltRequest(
            body="",
            query=f"code=foo&state={state}",
            headers={"cookie": [f"{oauth_flow.oauth_state_cookie_name}={state}"]},
        )
        resp = oauth_flow.handle_callback(req)
        assert resp.status == 200
        assert "https://www.example.com/completion" in resp.body

    def test_handle_callback_invalid_state(self):
        oauth_flow = OAuthFlow(
            client_id="111.222",
            client_secret="xxx",
            scopes=["chat:write", "commands"],
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
        )
        state = oauth_flow.issue_new_state(None)
        req = BoltRequest(
            body="",
            query=f"code=foo&state=invalid",
            headers={"cookie": [f"{oauth_flow.oauth_state_cookie_name}={state}"]},
        )
        resp = oauth_flow.handle_callback(req)
        assert resp.status == 400
