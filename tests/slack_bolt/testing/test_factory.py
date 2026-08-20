"""Unit tests for the shared request factory and dataclasses.

The core property under test: every request's ``wire_format`` + ``build_body()``
round-trips through Bolt's real ``parse_body`` back to the same payload dict --
i.e. the factory encodes requests exactly the way the receiver decodes them.
"""

import pytest

from slack_bolt.request.internals import parse_body
from slack_bolt.testing.factory import (
    ActionRequest,
    CommandRequest,
    SlackRequestFactory,
)
from slack_bolt.testing.internals import WireFormat, encode_wire_body


def _round_trip(request):
    body = request.build_body()
    content_type, raw_body = encode_wire_body(request.wire_format, body)
    return parse_body(raw_body, content_type)


class TestFactoryDefaultsAndOverrides:
    def test_suite_defaults_apply(self):
        f = SlackRequestFactory(team_id="T999", user_id="U999")
        cmd = f.command("/hi")
        assert cmd.team_id == "T999"
        assert cmd.user_id == "U999"
        assert cmd.command == "/hi"

    def test_per_call_override_beats_default(self):
        f = SlackRequestFactory(user_id="U999")
        assert f.command("/hi", user_id="U000").user_id == "U000"

    def test_default_that_is_not_a_field_is_ignored(self):
        # A suite default that no dataclass declares must be silently dropped,
        # never passed to the constructor (which would raise).
        f = SlackRequestFactory(not_a_field="x")
        assert f.command("/hi").command == "/hi"

    def test_direct_construction_without_factory(self):
        assert CommandRequest(command="/direct").command == "/direct"
        assert ActionRequest(action_id="btn", value="1").action_id == "btn"


class TestWireEncodingRoundTrips:
    def test_command_is_form_encoded(self):
        req = SlackRequestFactory().command("/hi", text="world")
        assert req.wire_format == WireFormat.FORM
        assert _round_trip(req) == req.build_body()

    def test_event_is_json_encoded(self):
        req = SlackRequestFactory().event("app_mention")
        assert req.wire_format == WireFormat.JSON
        parsed = _round_trip(req)
        assert parsed["type"] == "event_callback"
        assert parsed["event"]["type"] == "app_mention"
        assert parsed == req.build_body()

    def test_message_event(self):
        req = SlackRequestFactory().message("hello there")
        parsed = _round_trip(req)
        assert parsed["event"]["type"] == "message"
        assert parsed["event"]["text"] == "hello there"

    def test_action_is_payload_encoded(self):
        req = SlackRequestFactory().action(action_id="btn", value="1")
        assert req.wire_format == WireFormat.PAYLOAD
        parsed = _round_trip(req)
        assert parsed["type"] == "block_actions"
        assert parsed["actions"][0]["action_id"] == "btn"
        assert parsed["actions"][0]["value"] == "1"
        assert parsed == req.build_body()

    def test_shortcut(self):
        parsed = _round_trip(SlackRequestFactory().shortcut(callback_id="s1"))
        assert parsed["type"] == "shortcut"
        assert parsed["callback_id"] == "s1"

    def test_view_submission(self):
        parsed = _round_trip(SlackRequestFactory().view_submission(callback_id="v1"))
        assert parsed["type"] == "view_submission"
        assert parsed["view"]["callback_id"] == "v1"

    def test_view_closed_has_no_trigger_id(self):
        parsed = _round_trip(SlackRequestFactory().view_closed(callback_id="v1"))
        assert parsed["type"] == "view_closed"
        assert "trigger_id" not in parsed

    def test_options(self):
        parsed = _round_trip(SlackRequestFactory().options(action_id="sel"))
        assert parsed["type"] == "block_suggestion"
        assert parsed["action_id"] == "sel"

    def test_function(self):
        parsed = _round_trip(SlackRequestFactory().function(callback_id="fn"))
        assert parsed["event"]["type"] == "function_executed"
        assert parsed["event"]["function"]["callback_id"] == "fn"
        assert "function_execution_id" in parsed["event"]

    def test_unknown_wire_format_raises(self):
        with pytest.raises(ValueError):
            encode_wire_body("bogus", {})
