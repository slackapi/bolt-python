import pytest

from slack_bolt.request.internals import (
    extract_channel_id,
    extract_user_id,
    extract_team_id,
    extract_enterprise_id,
    parse_query,
    extract_is_enterprise_install,
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

    enterprise_no_channel_requests = [
        {
            "type": "shortcut",
            "token": "xxx",
            "action_ts": "1606983924.521157",
            "team": {"id": "T111", "domain": "ddd"},
            "user": {"id": "U111", "username": "use", "team_id": "T111"},
            "is_enterprise_install": False,
            "enterprise": {"id": "E111", "domain": "eee"},
            "callback_id": "run-socket-mode",
            "trigger_id": "111.222.xxx",
        },
    ]

    no_enterprise_no_channel_requests = [
        {
            "type": "shortcut",
            "token": "xxx",
            "action_ts": "1606983924.521157",
            "team": {"id": "T111", "domain": "ddd"},
            "user": {"id": "U111", "username": "use", "team_id": "T111"},
            "is_enterprise_install": False,
            # This may be "null" in Socket Mode
            "enterprise": None,
            "callback_id": "run-socket-mode",
            "trigger_id": "111.222.xxx",
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
        for req in self.enterprise_no_channel_requests:
            user_id = extract_user_id(req)
            assert user_id == "U111"
        for req in self.no_enterprise_no_channel_requests:
            user_id = extract_user_id(req)
            assert user_id == "U111"

    def test_team_id_extraction(self):
        for req in self.requests:
            team_id = extract_team_id(req)
            assert team_id == "T111"
        for req in self.enterprise_no_channel_requests:
            team_id = extract_team_id(req)
            assert team_id == "T111"
        for req in self.no_enterprise_no_channel_requests:
            team_id = extract_team_id(req)
            assert team_id == "T111"

    def test_enterprise_id_extraction(self):
        for req in self.requests:
            enterprise_id = extract_enterprise_id(req)
            assert enterprise_id == "E111"
        for req in self.enterprise_no_channel_requests:
            enterprise_id = extract_enterprise_id(req)
            assert enterprise_id == "E111"
        for req in self.no_enterprise_no_channel_requests:
            enterprise_id = extract_enterprise_id(req)
            assert enterprise_id is None

    def test_is_enterprise_install_extraction(self):
        for req in self.requests:
            should_be_false = extract_is_enterprise_install(req)
            assert should_be_false is False
        assert extract_is_enterprise_install({"is_enterprise_install": True}) is True
        assert extract_is_enterprise_install({"is_enterprise_install": False}) is False
        assert extract_is_enterprise_install({"is_enterprise_install": "true"}) is True
        assert extract_is_enterprise_install({"is_enterprise_install": "false"}) is False

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
