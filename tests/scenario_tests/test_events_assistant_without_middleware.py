import time

from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest, Say, SetStatus, SetTitle, SaveThreadContext, BoltContext
from slack_bolt.context.get_thread_context.get_thread_context import GetThreadContext
from slack_bolt.context.set_suggested_prompts.set_suggested_prompts import SetSuggestedPrompts
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.scenario_tests.test_events_assistant import (
    channel_message_changed_event_body,
    channel_user_message_event_body,
    message_changed_event_body,
    thread_context_changed_event_body,
    thread_started_event_body,
    user_message_event_body,
    user_message_event_body_with_assistant_thread,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


def assert_target_called(called: dict, timeout: float = 2.0):
    deadline = time.time() + timeout
    while called["value"] is False and time.time() < deadline:
        time.sleep(0.1)
    assert called["value"] is True


class TestEventsAssistantWithoutMiddleware:
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

    def test_thread_started(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.event("assistant_thread_started")
        def handle_assistant_thread_started(
            say: Say,
            set_status: SetStatus,
            set_title: SetTitle,
            set_suggested_prompts: SetSuggestedPrompts,
            get_thread_context: GetThreadContext,
            save_thread_context: SaveThreadContext,
            context: BoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            say("Hi, how can I help you today?")
            set_suggested_prompts(prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}])
            called["value"] = True

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_thread_context_changed(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.event("assistant_thread_context_changed")
        def handle_assistant_thread_context_changed(
            say: Say,
            set_status: SetStatus,
            set_title: SetTitle,
            set_suggested_prompts: SetSuggestedPrompts,
            get_thread_context: GetThreadContext,
            save_thread_context: SaveThreadContext,
            context: BoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say is not None
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            called["value"] = True

        request = BoltRequest(body=thread_context_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_user_message(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.message("")
        def handle_message(
            say: Say,
            set_status: SetStatus,
            set_title: SetTitle,
            set_suggested_prompts: SetSuggestedPrompts,
            get_thread_context: GetThreadContext,
            save_thread_context: SaveThreadContext,
            context: BoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            try:
                set_status("is typing...")
                say("Here you are!")
                called["value"] = True
            except Exception as e:
                say(f"Oops, something went wrong (error: {e}")

        request = BoltRequest(body=user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_user_message_with_assistant_thread(self):
        app = App(client=self.web_client)
        called = {"value": False}

        @app.message("")
        def handle_message(
            say: Say,
            set_status: SetStatus,
            set_title: SetTitle,
            set_suggested_prompts: SetSuggestedPrompts,
            get_thread_context: GetThreadContext,
            save_thread_context: SaveThreadContext,
            context: BoltContext,
        ):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None
            try:
                set_status("is typing...")
                say("Here you are!")
                called["value"] = True
            except Exception as e:
                say(f"Oops, something went wrong (error: {e}")

        request = BoltRequest(body=user_message_event_body_with_assistant_thread, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_message_changed(self):
        app = App(client=self.web_client)

        @app.event("message")
        def handle_message_event(
            say: Say,
            set_status: SetStatus,
            set_title: SetTitle,
            set_suggested_prompts: SetSuggestedPrompts,
            get_thread_context: GetThreadContext,
            save_thread_context: SaveThreadContext,
            context: BoltContext,
        ):
            assert context.thread_ts is not None
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None

        request = BoltRequest(body=message_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200

    def test_channel_user_message(self):
        app = App(client=self.web_client)

        @app.event("message")
        def handle_message_event(
            say: Say,
            set_status: SetStatus,
            set_title: SetTitle,
            set_suggested_prompts: SetSuggestedPrompts,
            get_thread_context: GetThreadContext,
            save_thread_context: SaveThreadContext,
            context: BoltContext,
        ):
            assert context.thread_ts is not None
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None

        request = BoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200

    def test_channel_message_changed(self):
        app = App(client=self.web_client)

        @app.event("message")
        def handle_message_event(
            say: Say,
            set_status: SetStatus,
            set_title: SetTitle,
            set_suggested_prompts: SetSuggestedPrompts,
            get_thread_context: GetThreadContext,
            save_thread_context: SaveThreadContext,
            context: BoltContext,
        ):
            assert context.thread_ts is not None
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_title is not None
            assert set_suggested_prompts is not None
            assert get_thread_context is not None
            assert save_thread_context is not None

        request = BoltRequest(body=channel_message_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
