import json

from slack_bolt.cli import get_hooks, get_manifest, start


class TestGetHooks:
    def test_get_manifest(self, capsys):
        get_manifest_module = get_manifest.__name__

        get_hooks.main()

        out, err = capsys.readouterr()
        json_response = json.loads(out)
        assert err is ""
        assert "hooks" in json_response
        assert get_manifest_module in json_response["hooks"]["get-manifest"]

    def test_start(self, capsys):
        start_module = start.__name__

        get_hooks.main()

        out, err = capsys.readouterr()
        json_response = json.loads(out)
        assert err is ""
        assert "hooks" in json_response
        assert start_module in json_response["hooks"]["start"]
