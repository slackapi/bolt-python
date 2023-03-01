import pytest
import os

from slack_bolt.cli.start import start
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestStart:

    working_directory = "tests/slack_bolt/cli/test_app"

    # signing_secret = "secret"
    # valid_token = "xoxb-valid"
    # mock_api_server_base_url = "http://localhost:8888"
    # web_client = WebClient(
    #     token=valid_token,
    #     base_url=mock_api_server_base_url,
    # )

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)
        os.environ["SLACK_CLI_XOXB"] = "xoxb-valid"
        os.environ["SLACK_CLI_XAPP"] = "xapp-xxx"

    def teardown_method(self):
        os.environ.pop("SLACK_CLI_XOXB", None)
        os.environ.pop("SLACK_CLI_XAPP", None)
        os.environ.pop("SLACK_CLI_CUSTOM_FILE_PATH", None)
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

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
