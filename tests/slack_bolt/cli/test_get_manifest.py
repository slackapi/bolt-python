import json
import pytest

from slack_bolt.cli.get_manifest import get_manifest


class TestGetManifest:
    def test_get_manifest(self):
        working_directory = "tests/slack_bolt/cli/test_app"

        manifest = get_manifest(working_directory)

        json_manifest = json.loads(manifest)
        assert "_metadata" in json_manifest

    def test_get_manifest_no_manifest(self, capsys):
        working_directory = "tests/slack_bolt/cli/test_app_no_manifest"

        with pytest.raises(SystemExit):
            get_manifest(working_directory)

        out, err = capsys.readouterr()
        assert err is ""
        assert out == "Manifest file not found!\nPath: tests/slack_bolt/cli/test_app_no_manifest\nFile: manifest.json\n"
