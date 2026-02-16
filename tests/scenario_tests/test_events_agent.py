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
