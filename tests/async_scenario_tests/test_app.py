import pytest
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from slack_bolt.async_app import AsyncApp
from slack_bolt.error import BoltError
from slack_bolt.oauth.async_oauth_flow import AsyncOAuthFlow
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncApp:
    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        restore_os_env(self.old_os_env)

    def test_signing_secret_absence(self):
        with pytest.raises(BoltError):
            AsyncApp(signing_secret=None, token="xoxb-xxx")
        with pytest.raises(BoltError):
            AsyncApp(signing_secret="", token="xoxb-xxx")

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
            signing_secret="valid", client_id="111.222", client_secret="valid"
        )
        assert app != None

    def test_valid_multi_auth_oauth_flow(self):
        oauth_flow = AsyncOAuthFlow(
            client_id="111.222",
            client_secret="valid",
            installation_store=FileInstallationStore(),
            oauth_state_store=FileOAuthStateStore(expiration_seconds=120),
        )
        app = AsyncApp(signing_secret="valid", oauth_flow=oauth_flow)
        assert app != None

    def test_valid_multi_auth_client_id_absence(self):
        with pytest.raises(BoltError):
            AsyncApp(signing_secret="valid", client_id=None, client_secret="valid")

    def test_valid_multi_auth_secret_absence(self):
        with pytest.raises(BoltError):
            AsyncApp(signing_secret="valid", client_id="111.222", client_secret=None)
