from time import sleep
from typing import Callable

from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest, Assistant, Say, SetSuggestedPrompts, SetStatus, BoltContext
from slack_bolt.middleware import Middleware
from slack_bolt.request import BoltRequest as BoltRequestType
from slack_bolt.response import BoltResponse
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestEventsAssistant:
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

    def test_assistant_threads(self):
        app = App(client=self.web_client)
        assistant = Assistant()

        state = {"called": False}

        def assert_target_called():
            count = 0
            while state["called"] is False and count < 20:
                sleep(0.1)
                count += 1
            assert state["called"] is True
            state["called"] = False

        @assistant.thread_started
        def start_thread(say: Say, set_suggested_prompts: SetSuggestedPrompts, context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            say("Hi, how can I help you today?")
            set_suggested_prompts(prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}])
            set_suggested_prompts(
                prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}], title="foo"
            )
            state["called"] = True

        @assistant.thread_context_changed
        def handle_thread_context_changed(context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            state["called"] = True

        @assistant.user_message
        def handle_user_message(say: Say, set_status: SetStatus, context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            try:
                set_status("is typing...")
                say("Here you are!")
                state["called"] = True
            except Exception as e:
                say(f"Oops, something went wrong (error: {e}")

        app.assistant(assistant)

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

        request = BoltRequest(body=thread_context_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

        request = BoltRequest(body=user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

        request = BoltRequest(body=user_message_event_body_with_assistant_thread, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

        request = BoltRequest(body=message_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200

        request = BoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 404

        request = BoltRequest(body=channel_message_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 404

    def test_assistant_threads_with_custom_listener_middleware(self):
        app = App(client=self.web_client)
        assistant = Assistant()

        state = {"called": False, "middleware_called": False}

        def assert_target_called():
            count = 0
            while state["called"] is False and count < 20:
                sleep(0.1)
                count += 1
            assert state["called"] is True
            state["called"] = False

        class TestMiddleware(Middleware):
            def process(self, *, req: BoltRequestType, resp: BoltResponse, next: Callable[[], BoltResponse]):
                state["middleware_called"] = True
                # Verify assistant utilities are available
                assert req.context.get("set_status") is not None
                assert req.context.get("set_title") is not None
                assert req.context.get("set_suggested_prompts") is not None
                assert req.context.get("get_thread_context") is not None
                assert req.context.get("save_thread_context") is not None
                return next()

        @assistant.thread_started(middleware=[TestMiddleware()])
        def start_thread(say: Say, set_suggested_prompts: SetSuggestedPrompts, context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            say("Hi, how can I help you today?")
            set_suggested_prompts(prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}])
            state["called"] = True

        @assistant.user_message(middleware=[TestMiddleware()])
        def handle_user_message(say: Say, set_status: SetStatus, context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            set_status("is typing...")
            say("Here you are!")
            state["called"] = True

        app.assistant(assistant)

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()
        assert state["middleware_called"] is True
        state["middleware_called"] = False

        request = BoltRequest(body=user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()
        assert state["middleware_called"] is True

    def test_assistant_events_without_assistant_middleware(self):
        app = App(client=self.web_client)

        state = {"called": False}

        def assert_target_called():
            count = 0
            while state["called"] is False and count < 20:
                sleep(0.1)
                count += 1
            assert state["called"] is True
            state["called"] = False

        @app.event("assistant_thread_started")
        def start_thread(say: Say, set_suggested_prompts: SetSuggestedPrompts, set_status: SetStatus, context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            assert set_status is not None
            assert set_suggested_prompts is not None
            assert context.get("set_title") is not None
            assert context.get("get_thread_context") is not None
            assert context.get("save_thread_context") is not None
            say("Hi, how can I help you today?")
            state["called"] = True

        @app.event("message")
        def handle_message(say: Say, context: BoltContext, body: dict):
            if context.get("set_status") is not None:
                assert say.thread_ts == context.thread_ts
                state["called"] = True

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

        request = BoltRequest(body=user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

        # Non-assistant events should not get kwargs injected
        request = BoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200

    def test_assistant_events_kwargs_disabled(self):
        app = App(client=self.web_client, attaching_agent_kwargs_enabled=False)

        state = {"called": False}

        def assert_target_called():
            count = 0
            while state["called"] is False and count < 20:
                sleep(0.1)
                count += 1
            assert state["called"] is True
            state["called"] = False

        @app.event("assistant_thread_started")
        def start_thread(context: BoltContext):
            assert context.get("set_status") is None
            assert context.get("set_title") is None
            assert context.get("set_suggested_prompts") is None
            assert context.get("get_thread_context") is None
            assert context.get("save_thread_context") is None
            state["called"] = True

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

    def test_assistant_threads_custom_middleware_can_short_circuit(self):
        app = App(client=self.web_client)
        assistant = Assistant()

        state = {"handler_called": False}

        class BlockingMiddleware(Middleware):
            def process(self, *, req: BoltRequestType, resp: BoltResponse, next: Callable[[], BoltResponse]):
                # Intentionally not calling next() to short-circuit
                return BoltResponse(status=200)

        @assistant.thread_started(middleware=[BlockingMiddleware()])
        def start_thread(say: Say, context: BoltContext):
            state["handler_called"] = True

        app.assistant(assistant)

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert state["handler_called"] is False


def build_payload(event: dict) -> dict:
    return {
        "token": "verification_token",
        "team_id": "T111",
        "enterprise_id": "E111",
        "api_app_id": "A111",
        "event": event,
        "type": "event_callback",
        "event_id": "Ev111",
        "event_time": 1599616881,
        "authorizations": [
            {
                "enterprise_id": "E111",
                "team_id": "T111",
                "user_id": "W111",
                "is_bot": True,
                "is_enterprise_install": False,
            }
        ],
    }


thread_started_event_body = build_payload(
    {
        "type": "assistant_thread_started",
        "assistant_thread": {
            "user_id": "W222",
            "context": {"channel_id": "C222", "team_id": "T111", "enterprise_id": "E111"},
            "channel_id": "D111",
            "thread_ts": "1726133698.626339",
        },
        "event_ts": "1726133698.665188",
    }
)

thread_context_changed_event_body = build_payload(
    {
        "type": "assistant_thread_context_changed",
        "assistant_thread": {
            "user_id": "W222",
            "context": {"channel_id": "C333", "team_id": "T111", "enterprise_id": "E111"},
            "channel_id": "D111",
            "thread_ts": "1726133698.626339",
        },
        "event_ts": "1726133698.665188",
    }
)


user_message_event_body = build_payload(
    {
        "user": "W222",
        "type": "message",
        "ts": "1726133700.887259",
        "text": "When Slack was released?",
        "team": "T111",
        "user_team": "T111",
        "source_team": "T222",
        "user_profile": {},
        "thread_ts": "1726133698.626339",
        "parent_user_id": "W222",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
    }
)


user_message_event_body_with_assistant_thread = build_payload(
    {
        "user": "W222",
        "type": "message",
        "ts": "1726133700.887259",
        "text": "When Slack was released?",
        "team": "T111",
        "user_team": "T111",
        "source_team": "T222",
        "user_profile": {},
        "thread_ts": "1726133698.626339",
        "parent_user_id": "W222",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "im",
        "assistant_thread": {"XXX": "YYY"},
    }
)

message_changed_event_body = build_payload(
    {
        "type": "message",
        "subtype": "message_changed",
        "message": {
            "text": "New chat",
            "subtype": "assistant_app_thread",
            "user": "U222",
            "type": "message",
            "edited": {},
            "thread_ts": "1726133698.626339",
            "reply_count": 2,
            "reply_users_count": 2,
            "latest_reply": "1726133700.887259",
            "reply_users": ["U222", "W111"],
            "is_locked": False,
            "assistant_app_thread": {"title": "When Slack was released?", "title_blocks": [], "artifacts": []},
            "ts": "1726133698.626339",
        },
        "previous_message": {
            "text": "New chat",
            "subtype": "assistant_app_thread",
            "user": "U222",
            "type": "message",
            "edited": {},
            "thread_ts": "1726133698.626339",
            "reply_count": 2,
            "reply_users_count": 2,
            "latest_reply": "1726133700.887259",
            "reply_users": ["U222", "W111"],
            "is_locked": False,
        },
        "channel": "D111",
        "hidden": True,
        "ts": "1726133701.028300",
        "event_ts": "1726133701.028300",
        "channel_type": "im",
    }
)

channel_user_message_event_body = build_payload(
    {
        "user": "W222",
        "type": "message",
        "ts": "1726133700.887259",
        "text": "When Slack was released?",
        "team": "T111",
        "user_team": "T111",
        "source_team": "T222",
        "user_profile": {},
        "thread_ts": "1726133698.626339",
        "parent_user_id": "W222",
        "channel": "D111",
        "event_ts": "1726133700.887259",
        "channel_type": "channel",
    }
)

channel_message_changed_event_body = build_payload(
    {
        "type": "message",
        "subtype": "message_changed",
        "message": {
            "text": "New chat",
            "user": "U222",
            "type": "message",
            "edited": {},
            "thread_ts": "1726133698.626339",
            "reply_count": 2,
            "reply_users_count": 2,
            "latest_reply": "1726133700.887259",
            "reply_users": ["U222", "W111"],
            "is_locked": False,
            "ts": "1726133698.626339",
        },
        "previous_message": {
            "text": "New chat",
            "user": "U222",
            "type": "message",
            "edited": {},
            "thread_ts": "1726133698.626339",
            "reply_count": 2,
            "reply_users_count": 2,
            "latest_reply": "1726133700.887259",
            "reply_users": ["U222", "W111"],
            "is_locked": False,
        },
        "channel": "D111",
        "hidden": True,
        "ts": "1726133701.028300",
        "event_ts": "1726133701.028300",
        "channel_type": "channel",
    }
)
