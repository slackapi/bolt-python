import time
import pytest
import os
from slack_bolt.cli.error import CliError

from slack_bolt.cli.start import start
from tests.adapter_tests.socket_mode.mock_socket_mode_server import start_socket_mode_server, stop_socket_mode_server
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
        start_socket_mode_server(self, 3012)

    def teardown_method(self):
        os.environ.pop("SLACK_CLI_XOXB", None)
        os.environ.pop("SLACK_CLI_XAPP", None)
        os.environ.pop("SLACK_APP_PATH", None)
        cleanup_mock_web_api_server(self)
        stop_socket_mode_server(self)
        restore_os_env(self.old_os_env)

    def test_start(self, capsys, caplog):

        start(self.working_directory)

        captured_sys = capsys.readouterr()

        assert "ran as __main__" in captured_sys.out
        assert "INFO A new session has been established" in caplog.text

    def test_start_with_entrypoint(self, capsys, caplog):
        os.environ["SLACK_APP_PATH"] = "my_app.py"
        start(self.working_directory)

        captured_sys = capsys.readouterr()

        assert "ran as __main__" in captured_sys.out
        assert "INFO A new session has been established" in caplog.text

    def test_start_no_entrypoint(self):
        working_directory = "tests/slack_bolt/cli"

        with pytest.raises(CliError) as e:
            start(working_directory)

        assert str(e.value) == f"Entrypoint not found!\nLooking for: {working_directory}/app.py"
