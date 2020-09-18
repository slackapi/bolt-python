import json
import re
from urllib.parse import quote

from slack_bolt import BoltRequest, BoltResponse
from slack_bolt.listener_matcher.builtins import block_action, action


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
