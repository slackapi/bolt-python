import json
import re
from urllib.parse import quote

from slack_bolt import BoltRequest, BoltResponse
from slack_bolt.listener_matcher.builtins import (
    block_action,
    action,
    workflow_step_execute,
)


class TestBuiltins:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_block_action(self):
        body = {
            "type": "block_actions",
            "actions": [
                {
                    "type": "button",
                    "action_id": "valid_action_id",
                    "block_id": "b",
                    "action_ts": "111.222",
                    "value": "v",
                }
            ],
        }
        raw_body = f"payload={quote(json.dumps(body))}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        req = BoltRequest(body=raw_body, headers=headers)
        resp = BoltResponse(status=404)

        assert block_action("valid_action_id").matches(req, resp) is True
        assert block_action("invalid_action_id").matches(req, resp) is False
        assert block_action(re.compile("valid_.+")).matches(req, resp) is True
        assert block_action(re.compile("invalid_.+")).matches(req, resp) is False

        assert action("valid_action_id").matches(req, resp) is True
        assert action("invalid_action_id").matches(req, resp) is False
        assert action(re.compile("valid_.+")).matches(req, resp) is True
        assert action(re.compile("invalid_.+")).matches(req, resp) is False

        assert action({"action_id": "valid_action_id"}).matches(req, resp) is True
        assert action({"action_id": "invalid_action_id"}).matches(req, resp) is False
        assert action({"action_id": re.compile("valid_.+")}).matches(req, resp) is True
        assert (
            action({"action_id": re.compile("invalid_.+")}).matches(req, resp) is False
        )

        assert (
            action({"action_id": "valid_action_id", "block_id": "b"}).matches(req, resp)
            is True
        )
        assert (
            action({"action_id": "invalid_action_id", "block_id": "b"}).matches(
                req, resp
            )
            is False
        )
        assert (
            action({"action_id": re.compile("valid_.+"), "block_id": "b"}).matches(
                req, resp
            )
            is True
        )
        assert (
            action({"action_id": re.compile("invalid_.+"), "block_id": "b"}).matches(
                req, resp
            )
            is False
        )

        assert (
            action({"action_id": "valid_action_id", "block_id": "bbb"}).matches(
                req, resp
            )
            is False
        )
        assert (
            action({"action_id": "invalid_action_id", "block_id": "bbb"}).matches(
                req, resp
            )
            is False
        )
        assert (
            action({"action_id": re.compile("valid_.+"), "block_id": "bbb"}).matches(
                req, resp
            )
            is False
        )
        assert (
            action({"action_id": re.compile("invalid_.+"), "block_id": "bbb"}).matches(
                req, resp
            )
            is False
        )

    def test_workflow_step_execute(self):
        payload = {
            "team_id": "T111",
            "enterprise_id": "E111",
            "api_app_id": "A111",
            "event": {
                "type": "workflow_step_execute",
                "callback_id": "copy_review",
                "workflow_step": {
                    "workflow_step_execute_id": "zzz-execution",
                    "workflow_id": "12345",
                    "workflow_instance_id": "11111",
                    "step_id": "111-222-333-444-555",
                    "inputs": {"taskName": {"value": "a"}},
                    "outputs": [
                        {"name": "taskName", "type": "text", "label": "Task Name"}
                    ],
                },
                "event_ts": "1601541373.225894",
            },
            "type": "event_callback",
            "event_id": "Ev111",
            "event_time": 1601541373,
        }

        request = BoltRequest(body=f"payload={quote(json.dumps(payload))}")

        m = workflow_step_execute("copy_review")
        assert m.matches(request, None) == True

        m = workflow_step_execute("copy_review_2")
        assert m.matches(request, None) == False

        m = workflow_step_execute(re.compile("copy_.+"))
        assert m.matches(request, None) == True
