import json
from time import time

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.app import App
from slack_bolt.request import BoltRequest
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestSlashCommand:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(
        token=valid_token,
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
            "content-type": ["application/x-www-form-urlencoded"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_valid_request(self) -> BoltRequest:
        timestamp, body = str(int(time())), json.dumps(slash_command_body)
        return BoltRequest(body=body, headers=self.build_headers(timestamp, body))

    def test_mock_server_is_running(self):
        resp = self.web_client.api_test()
        assert resp != None

    def test_success(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.command("/hello-world")(commander)

        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)

    def test_process_before_response(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            process_before_response=True,
        )
        app.command("/hello-world")(commander)

        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)

    def test_failure(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        request = self.build_valid_request()
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

        app.command("/another-one")(commander)
        response = app.dispatch(request)
        assert response.status == 404
        assert_auth_test_count(self, 1)

    def test_ssl_check_param_does_not_bypass_request_verification(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            ssl_check_enabled=False,
        )
        command_called = False

        def command_handler(ack):
            nonlocal command_called
            command_called = True
            ack()

        app.command("/hello-world")(command_handler)

        request = BoltRequest(
            body=f"{slash_command_body}&ssl_check=1",
            headers={
                "content-type": ["application/x-www-form-urlencoded"],
                "x-slack-signature": ["v0=invalid"],
                "x-slack-request-timestamp": ["0"],
            },
        )
        response = app.dispatch(request)
        assert response.status == 401
        assert response.body == """{"error": "invalid request"}"""
        assert command_called is False


slash_command_body = (
    "token=verification_token"
    "&team_id=T111"
    "&team_domain=test-domain"
    "&channel_id=C111"
    "&channel_name=random"
    "&user_id=W111"
    "&user_name=primary-owner"
    "&command=%2Fhello-world"
    "&text=Hi"
    "&enterprise_id=E111"
    "&enterprise_name=Org+Name"
    "&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT111%2F111%2Fxxxxx"
    "&trigger_id=111.111.xxx"
)


def commander(ack, body, payload, command):
    assert body == command
    assert payload == command
    ack()
