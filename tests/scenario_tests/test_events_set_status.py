import json
from threading import Event
from urllib.parse import quote

from slack_sdk.web import WebClient

from slack_bolt import App, BoltContext, BoltRequest
from slack_bolt.context.set_status.set_status import SetStatus
from slack_bolt.middleware.assistant import Assistant
from tests.mock_web_api_server import (
    assert_auth_test_count,
    assert_received_request_count,
    cleanup_mock_web_api_server,
    setup_mock_web_api_server,
)
from tests.scenario_tests.test_app import app_mention_event_body
from tests.scenario_tests.test_events_assistant import thread_started_event_body
from tests.scenario_tests.test_events_assistant import user_message_event_body as threaded_user_message_event_body
from tests.scenario_tests.test_message_bot import bot_message_event_payload, user_message_event_payload
from tests.scenario_tests.test_view_submission import body as view_submission_body
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestEventsSetStatus:
    valid_token = "xoxb-valid"
    mock_api_server_base_url = "http://localhost:8888"
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

    def test_set_status_injected_for_app_mention(self):
        app = App(client=self.web_client)

        @app.event("app_mention")
        def handle_mention(set_status: SetStatus, context: BoltContext):
            assert set_status is not None
            assert isinstance(set_status, SetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "C111"
            assert set_status.thread_ts == "1595926230.009600"
            set_status(status="Thinking...")

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, path="/assistant.threads.setStatus", min_count=1)

    def test_set_status_injected_for_threaded_message(self):
        app = App(client=self.web_client)

        @app.event("message")
        def handle_message(set_status: SetStatus, context: BoltContext):
            assert set_status is not None
            assert isinstance(set_status, SetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "D111"
            assert set_status.thread_ts == "1726133698.626339"
            set_status(status="Thinking...")

        request = BoltRequest(body=threaded_user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, path="/assistant.threads.setStatus", min_count=1)

    def test_set_status_in_user_message(self):
        app = App(client=self.web_client)

        @app.message("")
        def handle_user_message(set_status: SetStatus, context: BoltContext):
            assert set_status is not None
            assert isinstance(set_status, SetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "C111"
            assert set_status.thread_ts == "1610261659.001400"
            set_status(status="Thinking...")

        request = BoltRequest(body=user_message_event_payload, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, path="/assistant.threads.setStatus", min_count=1)

    def test_set_status_in_bot_message(self):
        app = App(client=self.web_client)

        @app.message("")
        def handle_bot_message(set_status: SetStatus, context: BoltContext):
            assert set_status is not None
            assert isinstance(set_status, SetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "C111"
            assert set_status.thread_ts == "1610261539.000900"
            set_status(status="Thinking...")

        request = BoltRequest(body=bot_message_event_payload, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, path="/assistant.threads.setStatus", min_count=1)

    def test_set_status_in_assistant_thread_started(self):
        app = App(client=self.web_client)
        assistant = Assistant()

        @assistant.thread_started
        def start_thread(set_status: SetStatus, context: BoltContext):
            assert set_status is not None
            assert isinstance(set_status, SetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "D111"
            assert set_status.thread_ts == "1726133698.626339"
            set_status(status="Thinking...")

        app.assistant(assistant)

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, path="/assistant.threads.setStatus", min_count=1)

    def test_set_status_in_assistant_user_message(self):
        app = App(client=self.web_client)
        assistant = Assistant()

        @assistant.user_message
        def handle_user_message(set_status: SetStatus, context: BoltContext):
            assert set_status is not None
            assert isinstance(set_status, SetStatus)
            assert set_status == context.set_status
            assert set_status.channel_id == "D111"
            assert set_status.thread_ts == "1726133698.626339"
            set_status(status="Thinking...")

        app.assistant(assistant)

        request = BoltRequest(body=threaded_user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert_received_request_count(self, path="/assistant.threads.setStatus", min_count=1)

    def test_set_status_is_none_for_view_submission(self):
        app = App(client=self.web_client, request_verification_enabled=False)
        listener_called = Event()

        @app.view("view-id")
        def handle_view(ack, set_status, context: BoltContext):
            ack()
            assert set_status is None
            assert context.set_status is None
            listener_called.set()

        request = BoltRequest(
            body=f"payload={quote(json.dumps(view_submission_body))}",
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert_auth_test_count(self, 1)
        assert listener_called.is_set()
