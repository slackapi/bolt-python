import json
from time import time
from urllib.parse import quote

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.adapter.wsgi import SlackRequestHandler
from slack_bolt.app import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from tests.mock_web_api_server import assert_auth_test_count, cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.mock_wsgi_server import WsgiTestServer
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestWsgiHttp:
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

    def build_raw_headers(self, timestamp: str, body: str = ""):
        content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
        return {
            "host": "123.123.123",
            "user-agent": "some slack thing",
            "content-length": str(len(body)),
            "accept": "application/json,*/*",
            "accept-encoding": "gzip,deflate",
            "content-type": content_type,
            "x-forwarded-for": "123.123.123",
            "x-forwarded-proto": "https",
            "x-slack-request-timestamp": timestamp,
            "x-slack-signature": self.generate_signature(body, timestamp),
        }

    def test_commands(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        def command_handler(ack):
            ack()

        app.command("/hello-world")(command_handler)

        body = (
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

        headers = self.build_raw_headers(str(int(time())), body)

        wsgi_server = WsgiTestServer(SlackRequestHandler(app))

        response = wsgi_server.http(method="POST", headers=headers, body=body)

        assert response.status == "200 OK"
        assert response.headers.get("content-type") == "text/plain;charset=utf-8"
        assert_auth_test_count(self, 1)

    def test_events(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        def event_handler():
            pass

        app.event("app_mention")(event_handler)

        body = json.dumps(
            {
                "token": "verification_token",
                "team_id": "T111",
                "enterprise_id": "E111",
                "api_app_id": "A111",
                "event": {
                    "client_msg_id": "9cbd4c5b-7ddf-4ede-b479-ad21fca66d63",
                    "type": "app_mention",
                    "text": "<@W111> Hi there!",
                    "user": "W222",
                    "ts": "1595926230.009600",
                    "team": "T111",
                    "channel": "C111",
                    "event_ts": "1595926230.009600",
                },
                "type": "event_callback",
                "event_id": "Ev111",
                "event_time": 1595926230,
                "authed_users": ["W111"],
            }
        )
        headers = self.build_raw_headers(str(int(time())), body)

        wsgi_server = WsgiTestServer(SlackRequestHandler(app))
        response = wsgi_server.http(method="POST", headers=headers, body=body)

        assert response.status == "200 OK"
        assert response.headers.get("content-type") == "text/plain;charset=utf-8"
        assert_auth_test_count(self, 1)

    def test_shortcuts(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        def shortcut_handler(ack):
            ack()

        app.shortcut("test-shortcut")(shortcut_handler)

        body_data = {
            "type": "shortcut",
            "token": "verification_token",
            "action_ts": "111.111",
            "team": {
                "id": "T111",
                "domain": "workspace-domain",
                "enterprise_id": "E111",
                "enterprise_name": "Org Name",
            },
            "user": {"id": "W111", "username": "primary-owner", "team_id": "T111"},
            "callback_id": "test-shortcut",
            "trigger_id": "111.111.xxxxxx",
        }

        body = f"payload={quote(json.dumps(body_data))}"
        headers = self.build_raw_headers(str(int(time())), body)

        wsgi_server = WsgiTestServer(SlackRequestHandler(app))
        response = wsgi_server.http(method="POST", headers=headers, body=body)

        assert response.status == "200 OK"
        assert response.headers.get("content-type") == "text/plain;charset=utf-8"
        assert_auth_test_count(self, 1)

    def test_oauth(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
            oauth_settings=OAuthSettings(
                client_id="111.111",
                client_secret="xxx",
                scopes=["chat:write", "commands"],
            ),
        )

        headers = self.build_raw_headers(str(int(time())))

        wsgi_server = WsgiTestServer(SlackRequestHandler(app))
        response = wsgi_server.http(method="GET", headers=headers, path="/slack/install")

        assert response.status == "200 OK"
        assert response.headers.get("content-type") == "text/html; charset=utf-8"
        assert "https://api.slack.com/oauth/v2/authorize?state=" in response.body

    def test_url_verification(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        body_data = {
            "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",
            "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",
            "type": "url_verification",
        }

        body = f"payload={quote(json.dumps(body_data))}"
        headers = self.build_raw_headers(str(int(time())), body)

        wsgi_server = WsgiTestServer(SlackRequestHandler(app))
        response = wsgi_server.http(
            method="POST",
            headers=headers,
            body=body,
        )

        assert response.status == "200 OK"
        assert response.headers.get("content-type") == "application/json;charset=utf-8"
        assert_auth_test_count(self, 1)

    def test_unsupported_method(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        body = ""
        headers = self.build_raw_headers(str(int(time())), "")

        wsgi_server = WsgiTestServer(SlackRequestHandler(app))
        response = wsgi_server.http(method="PUT", headers=headers, body=body)

        assert response.status == "404 Not Found"
        assert response.headers.get("content-type") == "text/plain;charset=utf-8"
        assert_auth_test_count(self, 1)
