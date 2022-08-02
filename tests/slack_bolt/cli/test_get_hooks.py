import json

from slack_bolt.cli import get_hooks, get_manifest, start


class TestGetHooks:
    def test_get_manifest(self, capsys):
        # given
        get_manifest_module = get_manifest.__name__

        # when
        get_hooks.main()

        # then
        out, err = capsys.readouterr()
        json_payload = json.loads(out)

        assert "hooks" in json_payload
        assert get_manifest_module in json_payload["hooks"]["get-manifest"]

    def test_start(self, capsys):
        # given
        start_module = start.__name__

        # when
        get_hooks.main()

        # then
        out, err = capsys.readouterr()
        json_payload = json.loads(out)

        assert "hooks" in json_payload
        assert start_module in json_payload["hooks"]["start"]
