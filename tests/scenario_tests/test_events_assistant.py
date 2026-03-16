import time

from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest, Assistant, Say, SetSuggestedPrompts, SetStatus, BoltContext
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


def assert_target_called(called: dict, expected: bool = True, timeout: float = 0.5):
    deadline = time.time() + timeout
    while called["value"] is not expected and time.time() < deadline:
        time.sleep(0.1)
    assert called["value"] is expected


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

    def test_thread_started(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.thread_started
        def start_thread(say: Say, set_suggested_prompts: SetSuggestedPrompts, set_status: SetStatus, context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert set_status.thread_ts == context.thread_ts
            assert say.thread_ts == context.thread_ts
            say("Hi, how can I help you today?")
            set_suggested_prompts(prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}])
            set_suggested_prompts(
                prompts=[{"title": "What does SLACK stand for?", "message": "What does SLACK stand for?"}], title="foo"
            )
            called["value"] = True

        app.assistant(assistant)

        request = BoltRequest(body=thread_started_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_thread_context_changed(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.thread_context_changed
        def handle_thread_context_changed(context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            called["value"] = True

        app.assistant(assistant)

        request = BoltRequest(body=thread_context_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_user_message(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.user_message
        def handle_user_message(say: Say, set_status: SetStatus, context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            try:
                set_status("is typing...")
                say("Here you are!")
                called["value"] = True
            except Exception as e:
                say(f"Oops, something went wrong (error: {e})")

        app.assistant(assistant)

        request = BoltRequest(body=user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_user_message_with_assistant_thread(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.user_message
        def handle_user_message(say: Say, set_status: SetStatus, context: BoltContext):
            assert context.channel_id == "D111"
            assert context.thread_ts == "1726133698.626339"
            assert say.thread_ts == context.thread_ts
            try:
                set_status("is typing...")
                say("Here you are!")
                called["value"] = True
            except Exception as e:
                say(f"Oops, something went wrong (error: {e})")

        app.assistant(assistant)

        request = BoltRequest(body=user_message_event_body_with_assistant_thread, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called)

    def test_message_changed(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.user_message
        def handle_user_message():
            called["value"] = True

        @assistant.bot_message
        def handle_bot_message():
            called["value"] = True

        app.assistant(assistant)

        request = BoltRequest(body=message_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called(called, key="user_message", expected=False)
        assert_target_called(called, key="bot_message", expected=False)

    def test_channel_user_message_ignored(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.user_message
        def handle_user_message():
            called["value"] = True

        @assistant.bot_message
        def handle_bot_message():
            called["value"] = True

        app.assistant(assistant)

        request = BoltRequest(body=channel_user_message_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 404
        assert_target_called(called, expected=False)

    def test_channel_message_changed_ignored(self):
        app = App(client=self.web_client)
        assistant = Assistant()
        called = {"value": False}

        @assistant.user_message
        def handle_user_message():
            called["value"] = True

        @assistant.bot_message
        def handle_bot_message():
            called["value"] = True

        app.assistant(assistant)

        request = BoltRequest(body=channel_message_changed_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 404
        assert_target_called(called, expected=False)


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
