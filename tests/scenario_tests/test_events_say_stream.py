import json
import time
from urllib.parse import quote

import pytest
from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest, BoltContext
from slack_bolt.context.say_stream.say_stream import SayStream
from slack_bolt.middleware.assistant import Assistant
from slack_bolt.warning import ExperimentalWarning
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.scenario_tests.test_app import app_mention_event_body
from tests.scenario_tests.test_events_assistant import (
    thread_started_event_body,
    user_message_event_body as threaded_user_message_event_body,
)
from tests.scenario_tests.test_message_bot import bot_message_event_payload, user_message_event_payload
from tests.scenario_tests.test_view_submission import body as view_submission_body
from tests.utils import remove_os_env_temporarily, restore_os_env


def assert_target_called(called: dict, timeout: float = 1.0):
    deadline = time.time() + timeout
    while called["value"] is not True and time.time() < deadline:
        time.sleep(0.1)
    assert called["value"] is True


class TestEventsSayStream:
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

    def test_say_stream_injected_for_app_mention(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.event("app_mention")
        def handle_mention(say_stream: SayStream, context: BoltContext):
            assert say_stream is not None
            assert isinstance(say_stream, SayStream)
            assert say_stream.channel_id == "C111"
            assert say_stream.thread_ts == "1595926230.009600"
            assert say_stream.team_id == context.team_id
            assert say_stream.user_id == context.user_id
            called["value"] = True

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_say_stream_injected_for_threaded_message(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.event("message")
        def handle_message(say_stream: SayStream, context: BoltContext):
            assert say_stream is not None
            assert isinstance(say_stream, SayStream)
            assert say_stream.channel_id == "D111"
            assert say_stream.thread_ts == "1726133698.626339"
            assert say_stream.team_id == context.team_id
            assert say_stream.user_id == context.user_id
            called["value"] = True

        request = BoltRequest(body=threaded_user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_say_stream_in_user_message(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.message("")
        def handle_user_message(say_stream: SayStream):
            assert say_stream is not None
            assert isinstance(say_stream, SayStream)
            assert say_stream.channel_id == "C111"
            assert say_stream.thread_ts == "1610261659.001400"
            called["value"] = True

        request = BoltRequest(body=user_message_event_payload, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_say_stream_in_bot_message(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.message("")
        def handle_user_message(say_stream: SayStream):
            assert say_stream is not None
            assert isinstance(say_stream, SayStream)
            assert say_stream.channel_id == "C111"
            assert say_stream.thread_ts == "1610261539.000900"
            called["value"] = True

        request = BoltRequest(body=bot_message_event_payload, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_say_stream_kwarg_emits_experimental_warning(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.event("app_mention")
        def handle_mention(say_stream: SayStream):
            with pytest.warns(ExperimentalWarning, match="say_stream is experimental"):
                say_stream()
            called["value"] = True

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_say_stream_in_assistant_thread_started(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.thread_started
        def start_thread(say_stream: SayStream):
            assert say_stream is not None
            assert isinstance(say_stream, SayStream)
            assert say_stream.channel_id == "D111"
            assert say_stream.thread_ts == "1726133698.626339"
            called["value"] = True

        app.assistant(assistant)

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_say_stream_in_assistant_user_message(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.user_message
        def handle_user_message(say_stream: SayStream):
            assert say_stream is not None
            assert isinstance(say_stream, SayStream)
            assert say_stream.channel_id == "D111"
            assert say_stream.thread_ts == "1726133698.626339"
            called["value"] = True

        app.assistant(assistant)

        request = BoltRequest(body=threaded_user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_say_stream_is_none_for_view_submission(self):
        app = App(client=self.web_client, request_verification_enabled=False)
        called = {"value": False}

        @app.view("view-id")
        def handle_view(ack, say_stream, context: BoltContext):
            ack()
            assert say_stream is None
            assert context.say_stream is None
            called["value"] = True

        request = BoltRequest(
            body=f"payload={quote(json.dumps(view_submission_body))}",
        )
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)
