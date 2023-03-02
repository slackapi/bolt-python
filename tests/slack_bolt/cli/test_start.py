import pytest
import os

from slack_bolt.cli.start import start
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env
from slack_sdk.errors import SlackApiError


class TestStart:

    working_directory = "tests/slack_bolt/cli/test_app"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        os.environ["SLACK_CLI_XOXB"] = "xoxb-valid"
        os.environ["SLACK_CLI_XAPP"] = "xapp-A111-222-xyz"
        setup_mock_web_api_server(self)

    def teardown_method(self):
        os.environ.pop("SLACK_CLI_XOXB", None)
        os.environ.pop("SLACK_CLI_XAPP", None)
        os.environ.pop("SLACK_CLI_CUSTOM_FILE_PATH", None)
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def test_start(self, capsys, caplog):
        with pytest.raises(SlackApiError):
            start(self.working_directory)

        out, err = capsys.readouterr()
        assert '"POST /apps.connections.open HTTP/1.1" 200' in err
        assert "ValueError: I/O operation on closed file." in err
        assert "{'ok': False, 'error': 'invalid_auth'}" in caplog.text
        assert "ran as __main__" not in out

    def test_start_with_entrypoint(self, capsys, caplog):
        os.environ["SLACK_CLI_CUSTOM_FILE_PATH"] = "my_app.py"
        with pytest.raises(SlackApiError):
            start(self.working_directory)

        out, err = capsys.readouterr()
        assert '"POST /apps.connections.open HTTP/1.1" 200' in err
        assert "ValueError: I/O operation on closed file." in err
        assert "{'ok': False, 'error': 'invalid_auth'}" in caplog.text
        assert "ran as __main__" not in out

    def test_start_no_entrypoint(self, capsys):
        working_directory = "tests/slack_bolt/cli"

        with pytest.raises(SystemExit):
            start(working_directory)

        out, err = capsys.readouterr()
        assert err is ""
        assert "Entrypoint not found!\nLooking for: tests/slack_bolt/cli/app.py" in out
