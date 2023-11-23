import json
import runpy

from slack_bolt.cli import get_hooks, get_manifest, start


class TestGetHooks:
    def test_get_manifest(self, capsys):

        runpy.run_module(get_hooks.__name__, run_name="__main__")

        out, err = capsys.readouterr()
        json_response = json.loads(out)
        assert err is ""
        assert "hooks" in json_response
        assert get_manifest.__name__ in json_response["hooks"]["get-manifest"]

    def test_start(self, capsys):

        runpy.run_module(get_hooks.__name__, run_name="__main__")

        out, err = capsys.readouterr()
        json_response = json.loads(out)
        assert err is ""
        assert "hooks" in json_response
        assert start.__name__ in json_response["hooks"]["start"]
