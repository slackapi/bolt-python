import json
import os
import runpy
import pytest
from slack_bolt.cli.error import CliError

from slack_bolt.cli import get_manifest


class TestGetManifest:
    def setup_method(self):
        self.cwd = os.getcwd()

    def teardown_method(self):
        os.chdir(self.cwd)

    def test_get_manifest_script(self, capsys):
        working_directory = "tests/scenario_tests/cli/test_app"
        os.chdir(working_directory)

        runpy.run_module(get_manifest.__name__, run_name="__main__")

        out, err = capsys.readouterr()
        assert err == ""
        assert {"_metadata": {}, "display_information": {"name": "Bolt app"}} == json.loads(out)

    def test_get_manifest_script_no_manifest(self):
        working_directory = "tests/scenario_tests/cli/test_app_no_manifest"
        os.chdir(working_directory)

        with pytest.raises(CliError) as e:
            runpy.run_module(get_manifest.__name__, run_name="__main__")

        assert str(e.value) == "Could not find a manifest.json file"
