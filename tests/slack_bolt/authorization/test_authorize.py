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

    def test_installation_store_legacy(self):
        installation_store = LegacyMemoryInstallationStore()
        authorize = InstallationStoreAuthorize(
            logger=installation_store.logger, installation_store=installation_store
        )
        assert authorize.find_installation_available is True
        context = BoltContext()
        context["client"] = WebClient(base_url=self.mock_api_server_base_url)
        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is False
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        assert self.mock_received_requests["/auth.test"] == 1

        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        assert self.mock_received_requests["/auth.test"] == 2

    def test_installation_store_cached_legacy(self):
        installation_store = LegacyMemoryInstallationStore()
        authorize = InstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            cache_enabled=True,
        )
        assert authorize.find_installation_available is True
        context = BoltContext()
        context["client"] = WebClient(base_url=self.mock_api_server_base_url)
        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is False
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        assert self.mock_received_requests["/auth.test"] == 1

        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        assert self.mock_received_requests["/auth.test"] == 1  # cached

    def test_installation_store_bot_only(self):
        installation_store = BotOnlyMemoryInstallationStore()
        authorize = InstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            bot_only=True,
        )
        assert authorize.find_installation_available is True
        assert authorize.bot_only is True
        context = BoltContext()
        context["client"] = WebClient(base_url=self.mock_api_server_base_url)
        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is True
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        assert self.mock_received_requests["/auth.test"] == 1

        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        assert self.mock_received_requests["/auth.test"] == 2

    def test_installation_store_cached_bot_only(self):
        installation_store = BotOnlyMemoryInstallationStore()
        authorize = InstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            cache_enabled=True,
            bot_only=True,
        )
        assert authorize.find_installation_available is True
        assert authorize.bot_only is True
        context = BoltContext()
        context["client"] = WebClient(base_url=self.mock_api_server_base_url)
        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is True
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        assert self.mock_received_requests["/auth.test"] == 1

        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        assert self.mock_received_requests["/auth.test"] == 1  # cached

    def test_installation_store(self):
        installation_store = MemoryInstallationStore()
        authorize = InstallationStoreAuthorize(
            logger=installation_store.logger, installation_store=installation_store
        )
        assert authorize.find_installation_available is True
        context = BoltContext()
        context["client"] = WebClient(base_url=self.mock_api_server_base_url)
        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token == "xoxp-valid"
        assert self.mock_received_requests["/auth.test"] == 1

        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token == "xoxp-valid"
        assert self.mock_received_requests["/auth.test"] == 2

    def test_installation_store_cached(self):
        installation_store = MemoryInstallationStore()
        authorize = InstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            cache_enabled=True,
        )
        assert authorize.find_installation_available is True
        context = BoltContext()
        context["client"] = WebClient(base_url=self.mock_api_server_base_url)
        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token == "xoxp-valid"
        assert self.mock_received_requests["/auth.test"] == 1

        result = authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token == "xoxp-valid"
        assert self.mock_received_requests["/auth.test"] == 1  # cached


class LegacyMemoryInstallationStore(InstallationStore):
    @property
    def logger(self) -> Logger:
        return logging.getLogger(__name__)

    def save(self, installation: Installation):
        pass

    def find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Bot]:
        return Bot(
            app_id="A111",
            enterprise_id="E111",
            team_id="T0G9PQBBK",
            bot_token="xoxb-valid-1",
            bot_id="B",
            bot_user_id="W",
            bot_scopes=["commands", "chat:write"],
            installed_at=datetime.datetime.now().timestamp(),
        )


class MemoryInstallationStore(LegacyMemoryInstallationStore):
    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        return Installation(
            app_id="A111",
            enterprise_id="E111",
            team_id="T0G9PQBBK",
            bot_token="xoxb-valid-2",
            bot_id="B",
            bot_user_id="W",
            bot_scopes=["commands", "chat:write"],
            user_id="W11111",
            user_token="xoxp-valid",
            user_scopes=["search:read"],
            installed_at=datetime.datetime.now().timestamp(),
        )


class BotOnlyMemoryInstallationStore(LegacyMemoryInstallationStore):
    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        raise ValueError
