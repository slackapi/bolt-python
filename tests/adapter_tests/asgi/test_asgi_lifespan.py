import pytest

from asgiref.testing import ApplicationCommunicator
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt.adapter.asgi import SlackRequestHandler
from slack_bolt.app import App
from tests.mock_asgi_server import AsgiTestServer
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsgiLifespan:
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

    @pytest.mark.asyncio
    async def test_startup(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        asgi_server = AsgiTestServer(SlackRequestHandler(app))

        response = await asgi_server.lifespan("startup")

        assert response.type == "lifespan.startup.complete"
        assert response.message == ""

    @pytest.mark.asyncio
    async def test_shutdown(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        asgi_server = AsgiTestServer(SlackRequestHandler(app))

        response = await asgi_server.lifespan("shutdown")

        assert response.type == "lifespan.shutdown.complete"
        assert response.message == ""

    @pytest.mark.asyncio
    async def test_full_lifespan_cycle(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        scope = {"type": "lifespan", "asgi": {"version": "3.0", "spec_version": "2.3"}}
        communicator = ApplicationCommunicator(SlackRequestHandler(app), scope)

        await communicator.send_input({"type": "lifespan.startup"})
        startup_response = await communicator.receive_output(timeout=1)
        assert startup_response["type"] == "lifespan.startup.complete"

        await communicator.send_input({"type": "lifespan.shutdown"})
        shutdown_response = await communicator.receive_output(timeout=1)
        assert shutdown_response["type"] == "lifespan.shutdown.complete"

    @pytest.mark.asyncio
    async def test_failed_event(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        asgi_server = AsgiTestServer(SlackRequestHandler(app))

        with pytest.raises(TypeError) as e:
            await asgi_server.websocket()

        assert e.match("Unsupported scope type: 'websocket'")
