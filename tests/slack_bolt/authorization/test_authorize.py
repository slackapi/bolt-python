import datetime
import logging
from logging import Logger
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.oauth import InstallationStore
from slack_sdk.oauth.installation_store import Bot, Installation

from slack_bolt import BoltContext
from slack_bolt.authorization.authorize import InstallationStoreAuthorize
from tests.mock_web_api_server import (
    cleanup_mock_web_api_server,
    setup_mock_web_api_server,
)


class TestAuthorize:
    mock_api_server_base_url = "http://localhost:8888"

    def setup_method(self):
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def test_installation_store(self):
        installation_store = MemoryInstallationStore()
        authorize = InstallationStoreAuthorize(
            logger=installation_store.logger, installation_store=installation_store
        )
        context = BoltContext()
        context["client"] = WebClient(base_url=self.mock_api_server_base_url)
        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert self.mock_received_requests["/auth.test"] == 1

        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert self.mock_received_requests["/auth.test"] == 2

    def test_installation_store_cached(self):
        installation_store = MemoryInstallationStore()
        authorize = InstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            cache_enabled=True,
        )
        context = BoltContext()
        context["client"] = WebClient(base_url=self.mock_api_server_base_url)
        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert self.mock_received_requests["/auth.test"] == 1

        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert self.mock_received_requests["/auth.test"] == 1  # cached


class MemoryInstallationStore(InstallationStore):
    @property
    def logger(self) -> Logger:
        return logging.getLogger(__name__)

    def save(self, installation: Installation):
        pass

    def find_bot(
        self, *, enterprise_id: Optional[str], team_id: Optional[str]
    ) -> Optional[Bot]:
        return Bot(
            app_id="A111",
            enterprise_id="E111",
            team_id="T0G9PQBBK",
            bot_token="xoxb-valid",
            bot_id="B",
            bot_user_id="W",
            bot_scopes=["commands", "chat:write"],
            installed_at=datetime.datetime.now().timestamp(),
        )
