import pytest

from slack_bolt.request.internals import (
    extract_channel_id,
    extract_user_id,
    extract_team_id,
    extract_enterprise_id,
    parse_query,
    parse_body,
)


class TestRequestInternals:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    # based on https://github.com/slackapi/bolt-js/blob/f8c25ffb5cd91827510bbc689e97556d2d5ad017/src/App.spec.ts#L1123
    requests = [
        {
            "event": {"channel": "C111", "user": "U111"},
            "team_id": "T111",
            "enterprise_id": "E111",
        },
        {
            "event": {"item": {"channel": "C111"}, "user": "U111", "item_user": "U222"},
            "team_id": "T111",
            "enterprise_id": "E111",
        },
        {
            "command": "/hello",
            "channel_id": "C111",
            "team_id": "T111",
            "enterprise_id": "E111",
            "user_id": "U111",
        },
        {
            "actions": [{}],
            "channel": {"id": "C111"},
            "user": {"id": "U111"},
            "team": {"id": "T111", "enterprise_id": "E111"},
        },
        {
            "type": "dialog_submission",
            "channel": {"id": "C111"},
            "user": {"id": "U111"},
            "team": {"id": "T111", "enterprise_id": "E111"},
        },
    ]

    def test_channel_id_extraction(self):
        for req in self.requests:
            channel_id = extract_channel_id(req)
            assert channel_id == "C111"

    def test_user_id_extraction(self):
        for req in self.requests:
            user_id = extract_user_id(req)
            assert user_id == "U111"

    def test_team_id_extraction(self):
        for req in self.requests:
            team_id = extract_team_id(req)
            assert team_id == "T111"

    def test_enterprise_id_extraction(self):
        for req in self.requests:
            team_id = extract_enterprise_id(req)
            assert team_id == "E111"

    def test_parse_query(self):
        expected = {"foo": ["bar"], "baz": ["123"]}

        q = parse_query("foo=bar&baz=123")
        assert q == expected

        q = parse_query({"foo": "bar", "baz": "123"})
        assert q == expected

        q = parse_query({"foo": ["bar"], "baz": ["123"]})
        assert q == expected

        with pytest.raises(ValueError):
            parse_query({"foo": {"bar": "ZZZ"}, "baz": {"123": "111"}})
