import pytest
import os
from slack_bolt.cli.error import CliError

from slack_bolt.cli.start import validate_env, get_main_file, get_main_path
from tests.utils import remove_os_env_temporarily, restore_os_env

SLACK_CLI_XOXB = "SLACK_CLI_XOXB"
SLACK_CLI_XAPP = "SLACK_CLI_XAPP"
SLACK_APP_PATH = "SLACK_APP_PATH"


class TestStart:

    working_directory = "tests/slack_bolt/cli/test_app"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        os.environ.pop(SLACK_CLI_XOXB, None)
        os.environ.pop(SLACK_CLI_XAPP, None)
        os.environ.pop(SLACK_APP_PATH, None)
        restore_os_env(self.old_os_env)

    def test_validate_env(self):
        os.environ[SLACK_CLI_XOXB] = "xoxb-valid"
        os.environ[SLACK_CLI_XAPP] = "xapp-A111-222-xyz"

        assert validate_env() == None

    def test_validate_env_with_missing_xoxb(self):
        os.environ[SLACK_CLI_XAPP] = "xapp-A111-222-xyz"
        with pytest.raises(CliError) as e:
            validate_env()
        assert str(e.value) == f"Missing local run bot token ({SLACK_CLI_XOXB})."

    def test_validate_env_with_missing_xapp(self):
        os.environ[SLACK_CLI_XOXB] = "xoxb-valid"
        with pytest.raises(CliError) as e:
            validate_env()
        assert str(e.value) == f"Missing local run app token ({SLACK_CLI_XAPP})."

    def test_get_main_file(self):
        assert get_main_file() == "app.py"

    def test_get_main_file_with_override(self):
        os.environ[SLACK_APP_PATH] = "my_app.py"
        assert get_main_file() == "my_app.py"

    def test_get_main_path(self):
        assert get_main_path("/dir") == "/dir/app.py"

    def test_get_main_path(self):
        os.environ[SLACK_APP_PATH] = "my_app.py"
        assert get_main_path("/dir") == "/dir/my_app.py"
