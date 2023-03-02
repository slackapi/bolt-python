import pytest

from slack_bolt.cli.utils import get_module_name, load_app
from slack_bolt.error import CliError
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env

from slack_bolt.app import App


class TestUtils:

    working_directory = "tests/slack_bolt/cli"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def test_get_module_name(self):
        path = f"{self.working_directory}/test_app/app.py"

        module_name = get_module_name(path)

        assert "app" == module_name

    def test_load_app(self):
        path = f"{self.working_directory}/test_load_app/app.py"

        app = load_app(path)

        assert isinstance(app, App)

    def test_load_app_no_app(self):
        path = f"{self.working_directory}/test_load_app"

        with pytest.raises(CliError):
            load_app(path)

    def test_load_app_multiple_apps(self):
        path = f"{self.working_directory}/test_load_app/apps.py"

        with pytest.raises(CliError):
            load_app(path)
