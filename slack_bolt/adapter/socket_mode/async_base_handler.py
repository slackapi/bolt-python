import asyncio
import logging
from typing import Union

from slack_sdk.socket_mode.async_client import AsyncBaseSocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest

from slack_bolt import App
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.util.utils import get_boot_message


class AsyncBaseSocketModeHandler:
    app: Union[App, AsyncApp]  # type: ignore
    client: AsyncBaseSocketModeClient

    async def handle(
        self, client: AsyncBaseSocketModeClient, req: SocketModeRequest
    ) -> None:
        raise NotImplementedError()

    async def connect_async(self):
        await self.client.connect()

    async def disconnect_async(self):
        await self.client.disconnect()

    async def close_async(self):
        await self.client.close()

    async def start_async(self):
        await self.connect_async()
        if self.app.logger.level > logging.INFO:
            print(get_boot_message())
        else:
            self.app.logger.info(get_boot_message())
        await asyncio.sleep(float("inf"))
