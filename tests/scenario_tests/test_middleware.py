import json
import logging
from time import time, sleep
from typing import Callable, Optional

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from slack_bolt import BoltResponse, CustomListenerMatcher
from slack_bolt.app import App
from slack_bolt.listener import CustomListener
from slack_bolt.listener.thread_runner import ThreadListenerRunner
from slack_bolt.middleware import Middleware
from slack_bolt.request import BoltRequest
from slack_bolt.request.payload_utils import is_shortcut
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count,
    assert_received_request_count,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestMiddleware:
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

    def build_request(self) -> BoltRequest:
        body = {
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
        timestamp, body = str(int(time())), json.dumps(body)
        return BoltRequest(
            body=body,
            headers={
                "content-type": ["application/json"],
                "x-slack-signature": [
                    self.signature_verifier.generate_signature(
                        body=body,
                        timestamp=timestamp,
                    )
                ],
                "x-slack-request-timestamp": [timestamp],
            },
        )

    def test_no_next_call(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.use(no_next)
        app.shortcut("test-shortcut")(just_ack)

        response = app.dispatch(self.build_request())
        assert response.status == 404
        assert_auth_test_count(self, 1)

    def test_next_call(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.use(just_next)
        app.shortcut("test-shortcut")(just_ack)

        response = app.dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        assert_auth_test_count(self, 1)

    def test_decorator_next_call(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        @app.middleware
        def just_next(next):
            next()

        app.shortcut("test-shortcut")(just_ack)

        response = app.dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        assert_auth_test_count(self, 1)

    def test_next_call_(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.use(just_next_)
        app.shortcut("test-shortcut")(just_ack)

        response = app.dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        assert_auth_test_count(self, 1)

    def test_decorator_next_call_(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )

        @app.middleware
        def just_next_(next_):
            next_()

        app.shortcut("test-shortcut")(just_ack)

        response = app.dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        assert_auth_test_count(self, 1)

    def test_class_call(self):
        class NextClass:
            def __call__(self, next):
                next()

        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.use(NextClass())
        app.shortcut("test-shortcut")(just_ack)

        response = app.dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        assert_auth_test_count(self, 1)

    def test_class_call_(self):
        class NextUnderscoreClass:
            def __call__(self, next_):
                next_()

        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        app.use(NextUnderscoreClass())
        app.shortcut("test-shortcut")(just_ack)

        response = app.dispatch(self.build_request())
        assert response.status == 200
        assert response.body == "acknowledged!"
        assert_auth_test_count(self, 1)

    def test_lazy_listener_middleware(self):
        app = App(
            client=self.web_client,
            signing_secret=self.signing_secret,
        )
        unmatch_middleware = LazyListenerStarter("xxxx")
        app.use(unmatch_middleware)

        response = app.dispatch(self.build_request())
        assert response.status == 404
        assert_auth_test_count(self, 1)

        my_middleware = LazyListenerStarter("test-shortcut")
        app.use(my_middleware)
        response = app.dispatch(self.build_request())
        assert response.status == 200
        count = 0
        while count < 20 and my_middleware.lazy_called is False:
            sleep(0.05)
        assert my_middleware.lazy_called is True


def just_ack(ack):
    ack("acknowledged!")


def no_next():
    pass


def just_next(next):
    next()


def just_next_(next_):
    next_()


class LazyListenerStarter(Middleware):
    lazy_called: bool
    callback_id: str

    def __init__(self, callback_id: str):
        self.lazy_called = False
        self.callback_id = callback_id

    def lazy_listener(self):
        self.lazy_called = True

    def process(self, *, req: BoltRequest, resp: BoltResponse, next: Callable[[], BoltResponse]) -> Optional[BoltResponse]:
        if is_shortcut(req.body):
            listener = CustomListener(
                app_name="test-app",
                ack_function=just_ack,
                lazy_functions=[self.lazy_listener],
                matchers=[
                    CustomListenerMatcher(
                        app_name="test-app",
                        func=lambda payload: payload.get("callback_id") == self.callback_id,
                    )
                ],
                middleware=[],
                base_logger=req.context.logger,
            )
            if listener.matches(req=req, resp=resp):
                listener_runner: ThreadListenerRunner = req.context.listener_runner
                response = listener_runner.run(
                    request=req,
                    response=resp,
                    listener_name="test",
                    listener=listener,
                )
                if response is not None:
                    return response
        next()
