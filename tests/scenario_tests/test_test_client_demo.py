"""Demonstration: the same scenarios as the hand-rolled scenario tests, using
``SlackTestClient``.

Compare with ``test_slash_command.py`` / ``test_block_actions.py``: there is no
localhost mock web server, no ``SignatureVerifier`` / ``build_headers`` /
``build_valid_request`` boilerplate, and no ``assert_auth_test_count`` plumbing.
The client signs the request, the recorder ("outbox") stands in for the network,
and assertions read the app's real outbound calls.
"""

from slack_bolt.app import App
from slack_bolt.testing import SlackRequestFactory, SlackTestClient
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestTestClientDemo:
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

    def test_slash_command(self):
        app = self._app()

        @app.command("/hello-world")
        def hello(ack, say):
            ack()
            say("Hi from the command!")

        f = SlackRequestFactory()
        with SlackTestClient(app) as client:
            response = client.send(f.command("/hello-world", text="Hi"))
            assert response.status == 200
            assert len(client.recorder.wait_for_api_calls("chat.postMessage", text="Hi from the command!")) == 1

    def test_unhandled_command_is_404(self):
        app = self._app()
        f = SlackRequestFactory()
        with SlackTestClient(app) as client:
            response = client.send(f.command("/not-registered"))
            assert response.status == 404

    def test_app_mention_event(self):
        app = self._app()

        @app.event("app_mention")
        def mention(say):
            say("You rang?")

        f = SlackRequestFactory()
        with SlackTestClient(app) as client:
            response = client.send(f.event("app_mention"))
            assert response.status == 200
            assert len(client.recorder.wait_for_api_calls("chat.postMessage", text="You rang?")) == 1

    def test_block_action(self):
        app = self._app()

        @app.action("a_button")
        def on_click(ack, respond):
            ack()
            respond("clicked!")

        f = SlackRequestFactory()
        with SlackTestClient(app) as client:
            response = client.send(f.action(action_id="a_button", value="1"))
            assert response.status == 200
            assert len(client.recorder.wait_for_responds(text="clicked!")) == 1
