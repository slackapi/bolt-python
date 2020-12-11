import pytest
from slack_sdk import WebClient
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from slack_bolt import App, Say
from slack_bolt.authorization import AuthorizeResult
from slack_bolt.error import BoltError
from slack_bolt.oauth import OAuthFlow
from slack_bolt.oauth.oauth_settings import OAuthSettings
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestApp:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url,)

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    @staticmethod
    def handle_app_mention(body, say: Say, payload, event):
        assert body["event"] == payload
        assert payload == event
        say("What's up?")

    # --------------------------
    # basic tests
    # --------------------------

    def test_signing_secret_absence(self):
        with pytest.raises(BoltError):
            App(signing_secret=None, token="xoxb-xxx")
        with pytest.raises(BoltError):
            App(signing_secret="", token="xoxb-xxx")

    def simple_listener(self, ack):
        ack()

    def test_listener_registration_error(self):
        app = App(signing_secret="valid", client=self.web_client)
        with pytest.raises(BoltError):
            app.action({"type": "invalid_type", "action_id": "a"})(self.simple_listener)

    # --------------------------
    # single team auth
    # --------------------------

    def test_valid_single_auth(self):
        app = App(signing_secret="valid", client=self.web_client)
        assert app != None

    def test_token_absence(self):
        with pytest.raises(BoltError):
            App(signing_secret="valid", token=None)
        with pytest.raises(BoltError):
            App(signing_secret="valid", token="")

    # --------------------------
    # multi teams auth
    # --------------------------

    def test_valid_multi_auth(self):
        app = App(
            signing_secret="valid",
            oauth_settings=OAuthSettings(client_id="111.222", client_secret="valid"),
        )
        assert app != None

    def test_valid_multi_auth_oauth_flow(self):
        oauth_flow = OAuthFlow(
            settings=OAuthSettings(
                client_id="111.222",
                client_secret="valid",
                installation_store=FileInstallationStore(),
                state_store=FileOAuthStateStore(expiration_seconds=120),
            )
        )
        app = App(signing_secret="valid", oauth_flow=oauth_flow)
        assert app != None

    def test_valid_multi_auth_client_id_absence(self):
        with pytest.raises(BoltError):
            App(
                signing_secret="valid",
                oauth_settings=OAuthSettings(client_id=None, client_secret="valid"),
            )

    def test_valid_multi_auth_secret_absence(self):
        with pytest.raises(BoltError):
            App(
                signing_secret="valid",
                oauth_settings=OAuthSettings(client_id="111.222", client_secret=None),
            )

    def test_authorize_conflicts(self):
        oauth_settings = OAuthSettings(
            client_id="111.222",
            client_secret="valid",
            installation_store=FileInstallationStore(),
            state_store=FileOAuthStateStore(expiration_seconds=120),
        )

        # no error with this
        App(signing_secret="valid", oauth_settings=oauth_settings)

        def authorize() -> AuthorizeResult:
            return AuthorizeResult(enterprise_id="E111", team_id="T111")

        with pytest.raises(BoltError):
            App(
                signing_secret="valid",
                authorize=authorize,
                oauth_settings=oauth_settings,
            )

        oauth_flow = OAuthFlow(settings=oauth_settings)
        # no error with this
        App(signing_secret="valid", oauth_flow=oauth_flow)

        with pytest.raises(BoltError):
            App(signing_secret="valid", authorize=authorize, oauth_flow=oauth_flow)

    def test_installation_store_conflicts(self):
        store1 = FileInstallationStore()
        store2 = FileInstallationStore()
        app = App(
            signing_secret="valid",
            oauth_settings=OAuthSettings(
                client_id="111.222", client_secret="valid", installation_store=store1,
            ),
            installation_store=store2,
        )
        assert app.installation_store is store1

        app = App(
            signing_secret="valid",
            oauth_flow=OAuthFlow(
                settings=OAuthSettings(
                    client_id="111.222",
                    client_secret="valid",
                    installation_store=store1,
                )
            ),
            installation_store=store2,
        )
        assert app.installation_store is store1

        app = App(
            signing_secret="valid",
            oauth_flow=OAuthFlow(
                settings=OAuthSettings(client_id="111.222", client_secret="valid",)
            ),
            installation_store=store1,
        )
        assert app.installation_store is store1
