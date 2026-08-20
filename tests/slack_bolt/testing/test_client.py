"""Unit tests for the sync ``SlackTestClient`` -- the real-pipeline dispatcher."""

from slack_bolt.app import App
from slack_bolt.testing import SlackRequestFactory, SlackTestClient
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestSlackTestClient:
    signing_secret = "secret"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        restore_os_env(self.old_os_env)

    def _app(self) -> App:
        return App(
            signing_secret=self.signing_secret,
            token="xoxb-valid",
            token_verification_enabled=False,
        )

    def test_command_dispatches_acks_and_captures_say(self):
        app = self._app()

        @app.command("/hi")
        def handle(ack, say):
            ack("ok")
            say("Hi!")

        f = SlackRequestFactory()
        with SlackTestClient(app) as client:
            resp = client.send(f.command("/hi"))
            assert resp.status == 200
            assert len(client.recorder.wait_for_api_calls("chat.postMessage", text="Hi!")) == 1

    def test_event_dispatches_and_captures_say(self):
        app = self._app()

        @app.event("app_mention")
        def handle(say):
            say("pong")

        f = SlackRequestFactory()
        with SlackTestClient(app) as client:
            resp = client.send(f.event("app_mention"))
            assert resp.status == 200
            assert len(client.recorder.wait_for_api_calls("chat.postMessage", text="pong")) == 1

    def test_action_captures_respond(self):
        app = self._app()

        @app.action("btn")
        def handle(ack, respond):
            ack()
            respond("got it")

        f = SlackRequestFactory()
        with SlackTestClient(app) as client:
            resp = client.send(f.action(action_id="btn"))
            assert resp.status == 200
            assert len(client.recorder.wait_for_responds(text="got it")) == 1

    def test_verify_false_uses_socket_mode(self):
        app = self._app()

        @app.command("/hi")
        def handle(ack):
            ack("ok")

        f = SlackRequestFactory()
        with SlackTestClient(app) as client:
            resp = client.send(f.command("/hi"), verify=False)
            assert resp.status == 200

    def test_wrong_signing_secret_fails_real_verification(self):
        app = self._app()

        @app.command("/hi")
        def handle(ack):
            ack("ok")

        f = SlackRequestFactory()
        with SlackTestClient(app, signing_secret="wrong-secret") as client:
            resp = client.send(f.command("/hi"))
            assert resp.status == 401

    def test_per_call_override_reaches_the_handler(self):
        app = self._app()

        @app.command("/hi")
        def handle(ack, command, say):
            ack()
            say(command["user_id"])  # echo the field so we can assert via the outbox

        f = SlackRequestFactory(user_id="U_DEFAULT")
        with SlackTestClient(app) as client:
            client.send(f.command("/hi", user_id="U_OVERRIDE"))
            assert len(client.recorder.wait_for_api_calls("chat.postMessage", text="U_OVERRIDE")) == 1
