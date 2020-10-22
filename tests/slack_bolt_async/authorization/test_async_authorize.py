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

from slack_bolt.authorization.async_authorize import AsyncInstallationStoreAuthorize
from slack_bolt.context.async_context import AsyncBoltContext
from tests.mock_web_api_server import (
    setup_mock_web_api_server,
    cleanup_mock_web_api_server,
)
from tests.utils import remove_os_env_temporarily, restore_os_env


class TestAsyncAuthorize:
    mock_api_server_base_url = "http://localhost:8888"
    client = AsyncWebClient(base_url=mock_api_server_base_url,)

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
    async def test_installation_store(self):
        installation_store = MemoryInstallationStore()
        authorize = AsyncInstallationStoreAuthorize(
            logger=installation_store.logger, installation_store=installation_store
        )
        context = AsyncBoltContext()
        context["client"] = self.client
        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert self.mock_received_requests["/auth.test"] == 1

        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert self.mock_received_requests["/auth.test"] == 2

    @pytest.mark.asyncio
    async def test_installation_store_cached(self):
        installation_store = MemoryInstallationStore()
        authorize = AsyncInstallationStoreAuthorize(
            logger=installation_store.logger,
            installation_store=installation_store,
            cache_enabled=True,
        )
        context = AsyncBoltContext()
        context["client"] = self.client
        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert self.mock_received_requests["/auth.test"] == 1

        result = await authorize(
            context=context, enterprise_id="E111", team_id="T0G9PQBBK", user_id="W11111"
        )
        assert result.bot_id == "BZYBOTHED"
        assert result.bot_user_id == "W23456789"
        assert self.mock_received_requests["/auth.test"] == 1  # cached


class MemoryInstallationStore(AsyncInstallationStore):
    @property
    def logger(self) -> Logger:
        return logging.getLogger(__name__)

    async def async_save(self, installation: Installation):
        pass

    async def async_find_bot(
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
