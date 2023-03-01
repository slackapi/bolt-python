import pytest
import os

from slack_bolt.cli.start import start, get_module_name, load_app


class TestStart:

    working_directory = "tests/slack_bolt/cli/test_app"

    def setup_method(self, method):
        os.environ["SLACK_CLI_XOXB"] = "xoxb-xxx"
        os.environ["SLACK_CLI_XAPP"] = "xapp-xxx"

    def teardown_method(self, method):
        os.environ.pop("SLACK_CLI_XOXB", None)
        os.environ.pop("SLACK_CLI_XAPP", None)
        os.environ.pop("SLACK_CLI_CUSTOM_FILE_PATH", None)

    def test_start(self, capsys):
        start(self.working_directory)

        out, err = capsys.readouterr()
        assert err is ""
        assert "app.py ran" in out

    def test_start_with_entrypoint(self, capsys):
        os.environ["SLACK_CLI_CUSTOM_FILE_PATH"] = "my_app.py"

        start(self.working_directory)

        out, err = capsys.readouterr()
        assert err is ""
        assert "my_app.py ran" in out

    def test_start_no_entrypoint(self, capsys):
        working_directory = "tests/slack_bolt/cli"

        with pytest.raises(SystemExit):
            start(working_directory)

        out, err = capsys.readouterr()
        assert err is ""
        assert "Entrypoint not found!\nLooking for: tests/slack_bolt/cli/app.py" in out

    def test_get_module_name(self, capsys):
        path = f"{self.working_directory}/app.py"

        module_name = get_module_name(path)

        assert "app" == module_name

    def test_get_module_name(self, capsys):
        path = f"{self.working_directory}/app.py"

        module_name = load_app(path)

        assert "app" == module_name
