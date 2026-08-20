"""Unit tests for ``AsyncSlackTestClient`` (``asyncio_mode = auto``)."""

from slack_bolt.async_app import AsyncApp
from slack_bolt.testing import SlackRequestFactory
from slack_bolt.testing.async_client import AsyncSlackTestClient
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncSlackTestClient:
    signing_secret = "secret"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        restore_os_env(self.old_os_env)

    def _app(self) -> AsyncApp:
        # AsyncApp does not verify the token at construction (no running loop),
        # so unlike the sync App it has no token_verification_enabled flag.
        return AsyncApp(
            signing_secret=self.signing_secret,
            token="xoxb-valid",
        )

    async def test_command_dispatches_acks_and_captures_say(self):
        app = self._app()

        @app.command("/hi")
        async def handle(ack, say):
            await ack("ok")
            await say("Hi!")

        f = SlackRequestFactory()
        async with AsyncSlackTestClient(app) as client:
            resp = await client.send(f.command("/hi"))
            assert resp.status == 200
            assert len(await client.recorder.wait_for_api_calls("chat.postMessage", text="Hi!")) == 1

    async def test_action_captures_respond(self):
        app = self._app()

        @app.action("btn")
        async def handle(ack, respond):
            await ack()
            await respond("got it")

        f = SlackRequestFactory()
        async with AsyncSlackTestClient(app) as client:
            resp = await client.send(f.action(action_id="btn"))
            assert resp.status == 200
            assert len(await client.recorder.wait_for_responds(text="got it")) == 1

    async def test_verify_false_uses_socket_mode(self):
        app = self._app()

        @app.command("/hi")
        async def handle(ack):
            await ack("ok")

        f = SlackRequestFactory()
        async with AsyncSlackTestClient(app) as client:
            resp = await client.send(f.command("/hi"), verify=False)
            assert resp.status == 200

    async def test_wrong_signing_secret_fails_real_verification(self):
        app = self._app()

        @app.command("/hi")
        async def handle(ack):
            await ack("ok")

        f = SlackRequestFactory()
        async with AsyncSlackTestClient(app, signing_secret="wrong-secret") as client:
            resp = await client.send(f.command("/hi"))
            assert resp.status == 401
