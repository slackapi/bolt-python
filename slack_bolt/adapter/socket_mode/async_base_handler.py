import asyncio
import logging

from slack_sdk.socket_mode.async_client import AsyncBaseSocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest


class AsyncBaseSocketModeHandler:
    client: AsyncBaseSocketModeClient

    async def handle(self, client: AsyncBaseSocketModeClient, req: SocketModeRequest) -> None:
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
            print("⚡️ Bolt app is running!")
        else:
            self.app.logger.info("⚡️ Bolt app is running!")
        await asyncio.sleep(float("inf"))
