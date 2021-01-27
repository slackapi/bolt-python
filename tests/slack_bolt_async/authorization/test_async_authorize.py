import asyncio
import datetime
import logging
from logging import Logger
from typing import Optional

import pytest
from slack_sdk.oauth.installation_store import Bot, Installation
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)
from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.authorization.async_authorize import (
    AsyncInstallationStoreAuthorize,
    AsyncAuthorize,
)
from slack_bolt.context.async_context import AsyncBoltContext
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
    assert_auth_test_count_async,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncAuthorize:
    mock_api_server_base_url = "http://localhost:8888"
    client = AsyncWebClient(
        base_url=mock_api_server_base_url,
    )

    @pytest.fixture
    def event_loop(self):
        old_os_env = remove_os_env_temporarily()
        try:
            setup_mock_web_api_server(self)
            loop = asyncio.get_event_loop()
            yield loop
            loop.close()
            cleanup_mock_web_api_server(self)
        finally:
            restore_os_env(old_os_env)

    @pytest.mark.asyncio
    async def test_root_class(self):
        authorize = AsyncAuthorize()
        with pytest.raises(NotImplementedError):
            await authorize(
                context=AsyncBoltContext(),
                enterprise_id="T111",
                team_id="T111",
                user_id="U111",
            )

    @pytest.mark.asyncio
    async def test_installation_store_legacy(self):
        installation_store = LegacyMemoryInstallationStore()
        authorize = AsyncInstallationStoreAuthorize(
            logger=installation_store.logger, installation_store=installation_store
        )
        assert authorize.find_installation_available is None
        context = AsyncBoltContext()
        context["client"] = self.client
        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is False
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        await assert_auth_test_count_async(self, 1)

        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        await assert_auth_test_count_async(self, 2)

    @pytest.mark.asyncio
    async def test_installation_store_cached_legacy(self):
        installation_store = LegacyMemoryInstallationStore()
        authorize = AsyncInstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            cache_enabled=True,
        )
        assert authorize.find_installation_available is None
        context = AsyncBoltContext()
        context["client"] = self.client
        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is False
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        await assert_auth_test_count_async(self, 1)

        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        await assert_auth_test_count_async(self, 1)  # cached

    @pytest.mark.asyncio
    async def test_installation_store_bot_only(self):
        installation_store = BotOnlyMemoryInstallationStore()
        authorize = AsyncInstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            bot_only=True,
        )
        assert authorize.find_installation_available is None
        assert authorize.bot_only is True
        context = AsyncBoltContext()
        context["client"] = self.client
        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is True
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        await assert_auth_test_count_async(self, 1)

        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        await assert_auth_test_count_async(self, 2)

    @pytest.mark.asyncio
    async def test_installation_store_cached_bot_only(self):
        installation_store = BotOnlyMemoryInstallationStore()
        authorize = AsyncInstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            cache_enabled=True,
            bot_only=True,
        )
        assert authorize.find_installation_available is None
        assert authorize.bot_only is True
        context = AsyncBoltContext()
        context["client"] = self.client
        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is True
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        await assert_auth_test_count_async(self, 1)

        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token is None
        await assert_auth_test_count_async(self, 1)  # cached

    @pytest.mark.asyncio
    async def test_installation_store(self):
        installation_store = MemoryInstallationStore()
        authorize = AsyncInstallationStoreAuthorize(
            logger=installation_store.logger, installation_store=installation_store
        )
        assert authorize.find_installation_available is None
        context = AsyncBoltContext()
        context["client"] = self.client
        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is True
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token == "xoxp-valid"
        await assert_auth_test_count_async(self, 1)

        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token == "xoxp-valid"
        await assert_auth_test_count_async(self, 2)

    @pytest.mark.asyncio
    async def test_installation_store_cached(self):
        installation_store = MemoryInstallationStore()
        authorize = AsyncInstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            cache_enabled=True,
        )
        assert authorize.find_installation_available is None
        context = AsyncBoltContext()
        context["client"] = self.client
        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert authorize.find_installation_available is True
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token == "xoxp-valid"
        await assert_auth_test_count_async(self, 1)

        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert result.user_token == "xoxp-valid"
        await assert_auth_test_count_async(self, 1)  # cached


class LegacyMemoryInstallationStore(AsyncInstallationStore):
    @property
    def logger(self) -> Logger:
        return logging.getLogger(__name__)

    async def async_save(self, installation: Installation):
        pass

    async def async_find_bot(
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
            bot_token="xoxb-valid",
            bot_id="B",
            bot_user_id="W",
            bot_scopes=["commands", "chat:write"],
            installed_at=datetime.datetime.now().timestamp(),
        )


class MemoryInstallationStore(LegacyMemoryInstallationStore):
    async def async_find_installation(
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
    async def async_find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        raise ValueError
