import json
import time

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.scenario_tests import test_block_actions, test_shortcut, test_slash_command, test_view_submission
from tests.slack_bolt.request import test_internals
from tests.utils import parse_request, remove_os_env_temporarily, restore_os_env

form_bodies = [
    test_block_actions.raw_body,
    test_shortcut.global_shortcut_raw_body,
    test_shortcut.message_shortcut_raw_body,
    test_slash_command.slash_command_body,
    test_view_submission.raw_body,
    test_view_submission.raw_response_url_body,
    test_view_submission.connect_channel_body,
]
json_bodies = [
    json.dumps(payload)
    for name, payloads in vars(test_internals.TestRequestInternals).items()
    if name.endswith("requests")
    for payload in payloads
]
signed_bodies = form_bodies + json_bodies

malformed_unsigned_bodies = [
    json.dumps(
        {
            "type": "event_callback",
            "event": {"type": "member_joined_channel", "user": "U0123456789", "channel": "C0123456789"},
        }
    ),
    '{"type": "event_callback", "event": ',
    "[1, 2, 3]",
    json.dumps({"user": "U0123456789", "view": "V0123456789", "enterprise": 1}),
]


def plain_values(context: dict) -> dict:
    return {
        key: value if isinstance(value, (str, bool, int, dict, list, type(None))) else type(value).__name__
        for key, value in context.items()
    }


class TestRequestParsing:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    signature_verifier = SignatureVerifier(signing_secret)
    web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def build_app(self, **kwargs) -> App:
        return App(client=self.web_client, signing_secret=self.signing_secret, **kwargs)

    def build_request(self, body: str) -> BoltRequest:
        timestamp = str(int(time.time()))
        content_type = "application/json" if body.startswith("{") else "application/x-www-form-urlencoded"
        return BoltRequest(
            body=body,
            headers={
                "content-type": [content_type],
                "x-slack-signature": [self.signature_verifier.generate_signature(body=body, timestamp=timestamp)],
                "x-slack-request-timestamp": [timestamp],
            },
        )

    def capture_after_dispatch(self, request: BoltRequest) -> dict:
        app = self.build_app()
        captured = {}

        @app.middleware
        def capture(context, body, next):
            captured["context"] = plain_values(context)
            captured["body"] = body
            captured["client_default_params"] = dict(context.client.default_params)
            next()

        app.dispatch(request)
        return captured

    def test_dispatch_matches_parsing_before_dispatch(self):
        for body in signed_bodies:
            parsed_before = self.capture_after_dispatch(parse_request(self.build_request(body)))
            parsed_in_dispatch = self.capture_after_dispatch(self.build_request(body))
            assert parsed_before != {}
            assert parsed_in_dispatch == parsed_before, body

    def test_new_request_is_unparsed(self):
        request = self.build_request(test_slash_command.slash_command_body)
        assert request.body == {}
        assert request.context.team_id is None

    def test_context_set_before_dispatch_wins_over_body(self):
        app = self.build_app()
        captured = {}

        @app.middleware
        def capture(context, next):
            captured["team_id"] = context.team_id
            captured["user_id"] = context.user_id
            captured["lambda_request"] = context["lambda_request"]
            next()

        request = self.build_request(test_slash_command.slash_command_body)
        request.context["team_id"] = "T_FROM_ADAPTER"
        request.context["lambda_request"] = {"source": "adapter"}
        app.dispatch(request)
        assert captured == {"team_id": "T_FROM_ADAPTER", "user_id": "W111", "lambda_request": {"source": "adapter"}}

    def test_malformed_unsigned_requests_are_rejected(self):
        app = self.build_app()
        for body in malformed_unsigned_bodies:
            request = BoltRequest(body=body, headers={"content-type": ["application/json"]})
            assert app.dispatch(request).status == 401

    def test_parsing_without_request_verification(self):
        app = self.build_app(request_verification_enabled=False)
        captured = {}

        @app.middleware
        def capture(context, next):
            captured["team_id"] = context.team_id
            next()

        app.dispatch(BoltRequest(body=test_slash_command.slash_command_body))
        assert captured["team_id"] == "T111"

    def test_signed_invalid_json_is_handled_by_the_error_handler(self):
        response = self.build_app().dispatch(self.build_request('{"type": "event_callback", '))
        assert response.status == 500

    def test_ssl_check(self):
        response = self.build_app().dispatch(BoltRequest(body="token=random&ssl_check=1"))
        assert response.status == 200
        assert response.body == ""

    def test_to_copyable_keeps_the_parsed_body(self):
        request = parse_request(self.build_request(test_slash_command.slash_command_body))
        copied = request.to_copyable()
        assert copied.body == request.body
        assert copied.body is not request.body
        assert copied.context.team_id == "T111"

    def test_lazy_listener_reads_the_body(self):
        app = self.build_app()
        lazy_bodies = []

        def just_ack(ack):
            ack()

        def read_body(body):
            lazy_bodies.append(body)

        app.command("/hello-world")(ack=just_ack, lazy=[read_body])
        response = app.dispatch(self.build_request(test_slash_command.slash_command_body))
        assert response.status == 200
        deadline = time.time() + 2
        while not lazy_bodies and time.time() < deadline:
            time.sleep(0.05)
        assert lazy_bodies[0]["command"] == "/hello-world"
