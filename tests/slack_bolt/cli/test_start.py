from cgi import test
import json
import pytest
import os

from slack_bolt.cli.start import start


class TestStart:
    def setup_method(self, method):
        os.environ["SLACK_CLI_XOXB"] = "xoxb-xxx"
        os.environ["SLACK_CLI_XAPP"] = "xapp-xxx"

    def teardown_method(self, method):
        os.environ.pop("SLACK_CLI_XOXB", None)
        os.environ.pop("SLACK_CLI_XAPP", None)
        os.environ.pop("SLACK_CLI_CUSTOM_FILE_PATH", None)

    def test_start(self, capsys):
        # given
        working_directory = "tests/slack_bolt/cli/test_directory"
        # when
        start(working_directory)
        out, err = capsys.readouterr()

        # then
        assert err is ""
        assert "app.py ran" in out

    def test_start_with_entrypoint(self, capsys):
        # given
        working_directory = "tests/slack_bolt/cli/test_directory"
        os.environ["SLACK_CLI_CUSTOM_FILE_PATH"] = "my_app.py"
        # when
        start(working_directory)
        out, err = capsys.readouterr()

        # then
        assert err is ""
        assert "my_app.py ran" in out

    def test_start_no_entrypoint(self, capsys):
        # given
        working_directory = "tests/slack_bolt/cli"
        # when
        with pytest.raises(SystemExit):
            start(working_directory)

        out, err = capsys.readouterr()
        # then
        assert err is ""
        assert "Entrypoint not found!\nLooking for: tests/slack_bolt/cli/app.py" in out
