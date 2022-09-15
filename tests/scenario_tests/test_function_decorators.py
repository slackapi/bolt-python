from typing import Callable

from slack_sdk import WebClient

from slack_bolt import App, Ack, BoltResponse
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class NoopAck(Ack):
    def __call__(self) -> BoltResponse:
        pass


class TestAppDecorators:
    signing_secret = "secret"
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
    web_client = WebClient(token=valid_token, base_url=mock_api_server_base_url)

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def test_decorators(self):
        app = App(signing_secret=self.signing_secret, client=self.web_client)
        ack = NoopAck()

        @app.function("c")
        def handle_function_events(body: dict):
            assert body is not None

        @handle_function_events.action("some-func-action-id")
        def handle_function_action(ack: Ack, body: dict):
            assert body is not None
            ack()

        handle_function_action(ack, {})
        assert isinstance(handle_function_action, Callable)

        @handle_function_events.view("some-callback-id")
        def handle_views(ack: Ack, body: dict):
            assert body is not None
            ack()

        handle_views(ack, {})
        assert isinstance(handle_views, Callable)

        handle_function_events({})
        assert isinstance(handle_function_events, Callable)

    def test_initialized_decorators(self):
        app = App(signing_secret=self.signing_secret, client=self.web_client)
        ack = NoopAck()

        func = app.function("c")

        @func
        def handle_function_events(body: dict):
            assert body is not None

        @handle_function_events.action("some-func-action-id")
        def handle_function_action(ack: Ack, body: dict):
            assert body is not None
            ack()

        handle_function_action(ack, {})
        assert isinstance(handle_function_action, Callable)

        handle_function_events({})
        assert isinstance(handle_function_events, Callable)

    def test_mixed_decorators(self):
        app = App(signing_secret=self.signing_secret, client=self.web_client)
        ack = NoopAck()

        func = app.function("c")

        @func
        def handle_function_events(body: dict):
            assert body is not None

        @func.action("some-func-action-id")
        def handle_function_action(ack: Ack, body: dict):
            assert body is not None
            ack()

        handle_function_action(ack, {})
        assert isinstance(handle_function_action, Callable)

        handle_function_events({})
        assert isinstance(handle_function_events, Callable)
