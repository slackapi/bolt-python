import json
from time import sleep, time
from typing import Optional

from slack_sdk.oauth import InstallationStore
from slack_sdk.oauth.installation_store import Installation
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest
from tests.mock_web_api_server import assert_auth_test_count, cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env

valid_token = "xoxb-valid"


class OrgAppInstallationStore(InstallationStore):
    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        assert enterprise_id == "E111"
        assert team_id is None
        return Installation(
            enterprise_id="E111",
            team_id=None,
            user_id=user_id,
            bot_token=valid_token,
            bot_id="B111",
        )


class Result:
    def __init__(self):
        self.called = False


class TestEventsOrgApps:
    signing_secret = "secret"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client: WebClient = WebClient(
        token=None,
        base_url=mock_api_server_base_url,
    )

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def test_team_access_granted(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            installation_store=OrgAppInstallationStore(),
        )

        event_payload = {
            "token": "verification-token",
            "enterprise_id": "E111",
            "api_app_id": "A111",
            "event": {
                "type": "team_access_granted",
                "team_ids": ["T111", "T222"],
                "event_ts": "111.222",
            },
            "type": "event_callback",
            "event_id": "Ev111",
            "event_time": 1606805974,
        }

        result = Result()

        @app.event("team_access_granted")
        def handle_app_mention(body):
            assert body == event_payload
            result.called = True

        timestamp, body = str(int(time())), json.dumps(event_payload)
        request: BoltRequest = BoltRequest(body=body, headers=self.build_headers(timestamp, body))
        response = app.dispatch(request)
        assert response.status == 200
        # auth.test API call must be skipped
        assert_auth_test_count(self, 1)
        sleep(0.5)  # wait a bit after auto ack()
        assert result.called is True

    def test_team_access_revoked(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            installation_store=OrgAppInstallationStore(),
        )

        event_payload = {
            "token": "verification-token",
            "enterprise_id": "E111",
            "api_app_id": "A111",
            "event": {
                "type": "team_access_revoked",
                "team_ids": ["T111", "T222"],
                "event_ts": "1606805732.987656",
            },
            "type": "event_callback",
            "event_id": "Ev111",
            "event_time": 1606805732,
        }

        result = Result()

        @app.event("team_access_revoked")
        def handle_app_mention(body):
            assert body == event_payload
            result.called = True

        timestamp, body = str(int(time())), json.dumps(event_payload)
        request: BoltRequest = BoltRequest(body=body, headers=self.build_headers(timestamp, body))
        response = app.dispatch(request)
        assert response.status == 200
        # auth.test API call must be skipped
        assert_auth_test_count(self, 0)
        sleep(0.5)  # wait a bit after auto ack()
        assert result.called is True

    def test_app_home_opened(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            installation_store=OrgAppInstallationStore(),
        )

        event_payload = {
            "token": "verification-token",
            "team_id": "T111",
            "enterprise_id": "E111",
            "api_app_id": "A111",
            "event": {
                "type": "app_home_opened",
                "user": "W111",
                "channel": "D111",
                "tab": "messages",
                "event_ts": "1606810927.510671",
            },
            "type": "event_callback",
            "event_id": "Ev111",
            "event_time": 1606810927,
            "authorizations": [
                {
                    "enterprise_id": "E111",
                    "team_id": None,
                    "user_id": "W111",
                    "is_bot": True,
                    "is_enterprise_install": True,
                }
            ],
            "is_ext_shared_channel": False,
        }

        result = Result()

        @app.event("app_home_opened")
        def handle_app_mention(body):
            assert body == event_payload
            result.called = True

        timestamp, body = str(int(time())), json.dumps(event_payload)
        request: BoltRequest = BoltRequest(body=body, headers=self.build_headers(timestamp, body))
        response = app.dispatch(request)
        assert response.status == 200
        # auth.test API call must be skipped
        assert_auth_test_count(self, 1)
        sleep(0.5)  # wait a bit after auto ack()
        assert result.called is True

    def test_message(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            installation_store=OrgAppInstallationStore(),
        )

        event_payload = {
            "token": "verification-token",
            "team_id": "T111",
            "enterprise_id": "E111",
            "api_app_id": "A111",
            "event": {
                "client_msg_id": "0186b75a-2ad4-4f36-8ccc-18608b0ac5d1",
                "type": "message",
                "text": "<@W222>",
                "user": "W111",
                "ts": "1606810819.000800",
                "team": "T111",
                "channel": "C111",
                "event_ts": "1606810819.000800",
                "channel_type": "channel",
            },
            "type": "event_callback",
            "event_id": "Ev111",
            "event_time": 1606810819,
            "authed_users": [],
            "authorizations": [
                {
                    "enterprise_id": "E111",
                    "team_id": None,
                    "user_id": "W222",
                    "is_bot": True,
                    "is_enterprise_install": True,
                }
            ],
            "is_ext_shared_channel": False,
            "event_context": "1-message-T111-C111",
        }

        result = Result()

        @app.event("message")
        def handle_app_mention(body):
            assert body == event_payload
            result.called = True

        timestamp, body = str(int(time())), json.dumps(event_payload)
        request: BoltRequest = BoltRequest(body=body, headers=self.build_headers(timestamp, body))
        response = app.dispatch(request)
        assert response.status == 200
        # auth.test API call must be skipped
        assert_auth_test_count(self, 1)
        sleep(0.5)  # wait a bit after auto ack()
        assert result.called is True
