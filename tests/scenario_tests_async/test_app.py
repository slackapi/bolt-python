import pytest
from slack_sdk import WebClient
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from slack_bolt.async_app import AsyncApp
from slack_bolt.authorization import AuthorizeResult
from slack_bolt.error import BoltError
from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncApp:
    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        restore_os_env(self.old_os_env)

    def non_coro_func(self, ack):
        ack()

    def test_non_coroutine_func_listener(self):
        app = AsyncApp(signing_secret="valid", token="xoxb-xxx")
        with pytest.raises(BoltError):
            app.action("a")(self.non_coro_func)

    async def simple_listener(self, ack):
        await ack()

    def test_listener_registration_error(self):
        app = AsyncApp(signing_secret="valid", token="xoxb-xxx")
        with pytest.raises(BoltError):
            app.action({"type": "invalid_type", "action_id": "a"})(self.simple_listener)

    # NOTE: We intentionally don't have this test in scenario_tests
    # to avoid having async dependencies in the tests.
    def test_invalid_client_type(self):
        with pytest.raises(BoltError):
            AsyncApp(signing_secret="valid", client=WebClient(token="xoxb-xxx"))

    # --------------------------
    # single team auth
    # --------------------------

    def test_valid_single_auth(self):
        app = AsyncApp(signing_secret="valid", token="xoxb-xxx")
        assert app != None

    def test_token_absence(self):
        with pytest.raises(BoltError):
            AsyncApp(signing_secret="valid", token=None)
        with pytest.raises(BoltError):
            AsyncApp(signing_secret="valid", token="")

    # --------------------------
    # multi teams auth
    # --------------------------

    def test_valid_multi_auth(self):
        app = AsyncApp(
            signing_secret="valid",
            oauth_settings=AsyncOAuthSettings(
                client_id="111.222", client_secret="valid"
            ),
        )
        assert app != None

    def test_valid_multi_auth_oauth_flow(self):
        oauth_flow = AsyncOAuthFlow(
            settings=AsyncOAuthSettings(
                client_id="111.222",
                client_secret="valid",
                installation_store=FileInstallationStore(),
                state_store=FileOAuthStateStore(expiration_seconds=120),
            )
        )
        app = AsyncApp(signing_secret="valid", oauth_flow=oauth_flow)
        assert app != None

    def test_valid_multi_auth_client_id_absence(self):
        with pytest.raises(BoltError):
            AsyncApp(
                signing_secret="valid",
                oauth_settings=AsyncOAuthSettings(
                    client_id=None, client_secret="valid"
                ),
            )

    def test_valid_multi_auth_secret_absence(self):
        with pytest.raises(BoltError):
            AsyncApp(
                signing_secret="valid",
                oauth_settings=AsyncOAuthSettings(
                    client_id="111.222", client_secret=None
                ),
            )

    def test_authorize_conflicts(self):
        oauth_settings = AsyncOAuthSettings(
            client_id="111.222",
            client_secret="valid",
            installation_store=FileInstallationStore(),
            state_store=FileOAuthStateStore(expiration_seconds=120),
        )

        # no error with this
        AsyncApp(signing_secret="valid", oauth_settings=oauth_settings)

        def authorize() -> AuthorizeResult:
            return AuthorizeResult(enterprise_id="E111", team_id="T111")

        with pytest.raises(BoltError):
            AsyncApp(
                signing_secret="valid",
                authorize=authorize,
                oauth_settings=oauth_settings,
            )

        oauth_flow = AsyncOAuthFlow(settings=oauth_settings)
        # no error with this
        AsyncApp(signing_secret="valid", oauth_flow=oauth_flow)

        with pytest.raises(BoltError):
            AsyncApp(signing_secret="valid", authorize=authorize, oauth_flow=oauth_flow)

    def test_installation_store_conflicts(self):
        store1 = FileInstallationStore()
        store2 = FileInstallationStore()
        app = AsyncApp(
            signing_secret="valid",
            oauth_settings=AsyncOAuthSettings(
                client_id="111.222", client_secret="valid", installation_store=store1,
            ),
            installation_store=store2,
        )
        assert app.installation_store is store1

        app = AsyncApp(
            signing_secret="valid",
            oauth_flow=AsyncOAuthFlow(
                settings=AsyncOAuthSettings(
                    client_id="111.222",
                    client_secret="valid",
                    installation_store=store1,
                )
            ),
            installation_store=store2,
        )
        assert app.installation_store is store1

        app = AsyncApp(
            signing_secret="valid",
            oauth_flow=AsyncOAuthFlow(
                settings=AsyncOAuthSettings(client_id="111.222", client_secret="valid",)
            ),
            installation_store=store1,
        )
        assert app.installation_store is store1
