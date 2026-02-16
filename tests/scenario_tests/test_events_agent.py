import json
from time import sleep

import pytest
from slack_sdk.web import WebClient

from slack_bolt import App, BoltRequest, BoltContext, BoltAgent
from slack_bolt.agent.agent import BoltAgent as BoltAgentDirect
from slack_bolt.warning import ExperimentalWarning
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestEventsAgent:
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

    def test_agent_injected_for_app_mention(self):
        app = App(client=self.web_client)

        state = {"called": False}

        def assert_target_called():
            count = 0
            while state["called"] is False and count < 20:
                sleep(0.1)
                count += 1
            assert state["called"] is True
            state["called"] = False

        @app.event("app_mention")
        def handle_mention(agent: BoltAgent, context: BoltContext):
            assert agent is not None
            assert isinstance(agent, BoltAgentDirect)
            assert context.channel_id == "C111"
            state["called"] = True

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

    def test_agent_available_in_action_listener(self):
        app = App(client=self.web_client)

        state = {"called": False}

        def assert_target_called():
            count = 0
            while state["called"] is False and count < 20:
                sleep(0.1)
                count += 1
            assert state["called"] is True
            state["called"] = False

        @app.action("test_action")
        def handle_action(ack, agent: BoltAgent):
            ack()
            assert agent is not None
            assert isinstance(agent, BoltAgentDirect)
            state["called"] = True

        request = BoltRequest(body=json.dumps(action_event_body), mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()

    def test_agent_thread_ts_from_event_in_thread(self):
        """Agent gets thread_ts from event when in a thread."""
        app = App(client=self.web_client)

        state = {"thread_ts": None}

        def assert_target_called():
            count = 0
            while state["thread_ts"] is None and count < 20:
                sleep(0.1)
                count += 1
            assert state["thread_ts"] is not None

        @app.event("app_mention")
        def handle_mention(agent: BoltAgent):
            state["thread_ts"] = agent._thread_ts

        request = BoltRequest(body=app_mention_in_thread_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()
        # Should use event.thread_ts (the thread root), not event.ts
        assert state["thread_ts"] == "1111111111.111111"

    def test_agent_thread_ts_falls_back_to_ts(self):
        """Agent falls back to event.ts when not in a thread."""
        app = App(client=self.web_client)

        state = {"thread_ts": None}

        def assert_target_called():
            count = 0
            while state["thread_ts"] is None and count < 20:
                sleep(0.1)
                count += 1
            assert state["thread_ts"] is not None

        @app.event("app_mention")
        def handle_mention(agent: BoltAgent):
            state["thread_ts"] = agent._thread_ts

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()
        # Should fall back to event.ts since no thread_ts
        assert state["thread_ts"] == "1234567890.123456"

    def test_agent_kwarg_emits_experimental_warning(self):
        app = App(client=self.web_client)

        state = {"called": False}

        def assert_target_called():
            count = 0
            while state["called"] is False and count < 20:
                sleep(0.1)
                count += 1
            assert state["called"] is True
            state["called"] = False

        @app.event("app_mention")
        def handle_mention(agent: BoltAgent):
            state["called"] = True

        request = BoltRequest(body=app_mention_event_body, mode="socket_mode")
        with pytest.warns(ExperimentalWarning, match="agent listener argument is experimental"):
            response = app.dispatch(request)
        assert response.status == 200
        assert_target_called()


# ---- Test event bodies ----


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


app_mention_event_body = build_payload(
    {
        "type": "app_mention",
        "user": "W222",
        "text": "<@W111> hello",
        "ts": "1234567890.123456",
        "channel": "C111",
        "event_ts": "1234567890.123456",
    }
)

app_mention_in_thread_body = build_payload(
    {
        "type": "app_mention",
        "user": "W222",
        "text": "<@W111> hello in thread",
        "ts": "2222222222.222222",
        "thread_ts": "1111111111.111111",  # Thread root timestamp
        "channel": "C111",
        "event_ts": "2222222222.222222",
    }
)

action_event_body = {
    "type": "block_actions",
    "user": {"id": "W222", "username": "test_user", "name": "test_user", "team_id": "T111"},
    "api_app_id": "A111",
    "token": "verification_token",
    "container": {"type": "message", "message_ts": "1234567890.123456", "channel_id": "C111", "is_ephemeral": False},
    "channel": {"id": "C111", "name": "test-channel"},
    "team": {"id": "T111", "domain": "test"},
    "enterprise": {"id": "E111", "name": "test"},
    "trigger_id": "111.222.xxx",
    "actions": [
        {
            "type": "button",
            "block_id": "b",
            "action_id": "test_action",
            "text": {"type": "plain_text", "text": "Button"},
            "action_ts": "1234567890.123456",
        }
    ],
}
