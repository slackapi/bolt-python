"""Demonstration: the async twin of ``test_test_client_demo.py``.

Same shape, awaited. ``asyncio_mode = auto`` (pyproject.toml) means these
``async def`` tests run without an explicit marker.
"""

from slack_bolt.async_app import AsyncApp
from slack_bolt.testing import SlackRequestFactory
from slack_bolt.testing.async_client import AsyncSlackTestClient
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncTestClientDemo:
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

    async def test_slash_command(self):
        app = self._app()

        @app.command("/hello-world")
        async def hello(ack, say):
            await ack()
            await say("Hi from the command!")

        f = SlackRequestFactory()
        async with AsyncSlackTestClient(app) as client:
            response = await client.send(f.command("/hello-world", text="Hi"))
            assert response.status == 200
            assert len(await client.recorder.wait_for_api_calls("chat.postMessage", text="Hi from the command!")) == 1

    async def test_app_mention_event(self):
        app = self._app()

        @app.event("app_mention")
        async def mention(say):
            await say("You rang?")

        f = SlackRequestFactory()
        async with AsyncSlackTestClient(app) as client:
            response = await client.send(f.event("app_mention"))
            assert response.status == 200
            assert len(await client.recorder.wait_for_api_calls("chat.postMessage", text="You rang?")) == 1

    async def test_block_action(self):
        app = self._app()

        @app.action("a_button")
        async def on_click(ack, respond):
            await ack()
            await respond("clicked!")

        f = SlackRequestFactory()
        async with AsyncSlackTestClient(app) as client:
            response = await client.send(f.action(action_id="a_button", value="1"))
            assert response.status == 200
            assert len(await client.recorder.wait_for_responds(text="clicked!")) == 1
