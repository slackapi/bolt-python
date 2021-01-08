import json
from time import time, sleep
from typing import Callable

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest, Say, Ack, BoltContext
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAppUsingMethodsInClass:
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

    def run_app_and_verify(self, app: App):
        payload = {
            "type": "message_action",
            "token": "verification_token",
            "action_ts": "1583637157.207593",
            "team": {
                "id": "T111",
                "domain": "test-test",
                "enterprise_id": "E111",
                "enterprise_name": "Org Name",
            },
            "user": {"id": "W111", "name": "test-test"},
            "channel": {"id": "C111", "name": "dev"},
            "callback_id": "test-shortcut",
            "trigger_id": "111.222.xxx",
            "message_ts": "1583636382.000300",
            "message": {
                "client_msg_id": "zzzz-111-222-xxx-yyy",
                "type": "message",
                "text": "<@W222> test",
                "user": "W111",
                "ts": "1583636382.000300",
                "team": "T111",
                "blocks": [
                    {
                        "type": "rich_text",
                        "block_id": "d7eJ",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "user", "user_id": "U222"},
                                    {"type": "text", "text": " test"},
                                ],
                            }
                        ],
                    }
                ],
            },
            "response_url": "https://hooks.slack.com/app/T111/111/xxx",
        }

        timestamp, body = str(int(time())), f"payload={json.dumps(payload)}"
        request: BoltRequest = BoltRequest(
            body=body,
            headers={
                "content-type": ["application/x-www-form-urlencoded"],
                "x-slack-signature": [
                    self.signature_verifier.generate_signature(
                        body=body,
                        timestamp=timestamp,
                    )
                ],
                "x-slack-request-timestamp": [timestamp],
            },
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert self.mock_received_requests["/auth.test"] == 1
        sleep(0.5)  # wait a bit after auto ack()
        assert self.mock_received_requests["/chat.postMessage"] == 1

    def test_class_methods(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        app.use(AwesomeClass.class_middleware)
        app.shortcut("test-shortcut")(AwesomeClass.class_method)
        self.run_app_and_verify(app)

    def test_class_methods_uncommon_name(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        app.use(AwesomeClass.class_middleware)
        app.shortcut("test-shortcut")(AwesomeClass.class_method2)
        self.run_app_and_verify(app)

    def test_instance_methods(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        awesome = AwesomeClass("Slackbot")
        app.use(awesome.instance_middleware)
        app.shortcut("test-shortcut")(awesome.instance_method)
        self.run_app_and_verify(app)

    def test_instance_methods_uncommon_name(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        awesome = AwesomeClass("Slackbot")
        app.use(awesome.instance_middleware)
        app.shortcut("test-shortcut")(awesome.instance_method2)
        self.run_app_and_verify(app)

    def test_static_methods(self):
        app = App(client=self.web_client, signing_secret=self.signing_secret)
        app.use(AwesomeClass.static_middleware)
        app.shortcut("test-shortcut")(AwesomeClass.static_method)
        self.run_app_and_verify(app)


class AwesomeClass:
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def class_middleware(cls, next: Callable):
        next()

    def instance_middleware(self, next: Callable):
        next()

    @staticmethod
    def static_middleware(next):
        next()

    @classmethod
    def class_method(cls, context: BoltContext, say: Say, ack: Ack):
        ack()
        say(f"Hello <@{context.user_id}>!")

    @classmethod
    def class_method2(xyz, context: BoltContext, say: Say, ack: Ack):
        ack()
        say(f"Hello <@{context.user_id}>!")

    def instance_method(self, context: BoltContext, say: Say, ack: Ack):
        ack()
        say(f"Hello <@{context.user_id}>! My name is {self.name}")

    def instance_method2(whatever, context: BoltContext, say: Say, ack: Ack):
        ack()
        say(f"Hello <@{context.user_id}>! My name is {whatever.name}")

    @staticmethod
    def static_method(context: BoltContext, say: Say, ack: Ack):
        ack()
        say(f"Hello <@{context.user_id}>!")
