from threading import Event

from slack_bolt import App, Assistant, BoltRequest
from slack_bolt.authorization import AuthorizeResult
from slack_bolt.context.assistant import assistant_utilities
from slack_bolt.context.assistant.thread_context import AssistantThreadContext
from slack_bolt.context.assistant.thread_context_store.store import AssistantThreadContextStore
from slack_sdk import WebClient
from tests.scenario_tests.test_events_assistant import user_message_event_body


class RecordingDefaultAssistantThreadContextStore(AssistantThreadContextStore):
    def __init__(self, context, seen_bot_user_ids):
        self.seen_bot_user_ids = seen_bot_user_ids
        self.seen_bot_user_ids.append(context.bot_user_id)

    def find(self, *, channel_id: str, thread_ts: str):
        return AssistantThreadContext({"channel_id": "C222", "team_id": "T111"})

    def save(self, *, channel_id: str, thread_ts: str, context):
        pass


class TestAppAssistant:
    def test_user_message_get_thread_context_store_is_initialized_after_authorize(self, monkeypatch):
        seen_bot_user_ids = []

        def build_store(context):
            return RecordingDefaultAssistantThreadContextStore(context, seen_bot_user_ids)

        monkeypatch.setattr(
            assistant_utilities,
            "DefaultAssistantThreadContextStore",
            build_store,
        )

        def authorize(context, enterprise_id, team_id, user_id):
            return AuthorizeResult(
                enterprise_id=enterprise_id,
                team_id=team_id,
                bot_user_id="W23456789",
                bot_id="B111",
                bot_token="xoxb-valid",
            )

        app = App(
            client=WebClient(token=None),
            authorize=authorize,
            process_before_response=True,
        )
        assistant = Assistant()
        listener_called = Event()

        @assistant.user_message
        def handle_user_message(get_thread_context):
            assert get_thread_context() == {"channel_id": "C222", "team_id": "T111"}
            listener_called.set()

        app.assistant(assistant)

        response = app.dispatch(BoltRequest(body=user_message_event_body, mode="socket_mode"))

        assert response.status == 200
        assert listener_called.is_set()
        assert seen_bot_user_ids == ["W23456789"]
