import pytest
import os

from slack_sdk import WebClient

from slack_bolt.cli.app_loader import get_module_name, load_app
from slack_bolt.error import CliError
from tests.mock_web_api_server import cleanup_mock_web_api_server, setup_mock_web_api_server
from tests.utils import remove_os_env_temporarily, restore_os_env

from slack_bolt.app import App


class TestLoader:

    working_directory = "tests/slack_bolt/cli/test_app"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)
        restore_os_env(self.old_os_env)

    def test_get_module_name(self):
        path = f"{self.working_directory}/app.py"

        module_name = get_module_name(path)

        assert "app" == module_name

    def test_load_app(self):
        path = f"{self.working_directory}/load_app/app.py"

        app = load_app(path)

        assert isinstance(app, App)

    def test_load_app_no_app(self):
        path = f"{self.working_directory}"

        with pytest.raises(CliError):
            load_app(path)

    def test_load_app_multiple_appsl(self):
        path = f"{self.working_directory}/load_app/apps.py"

        with pytest.raises(CliError):
            load_app(path)
