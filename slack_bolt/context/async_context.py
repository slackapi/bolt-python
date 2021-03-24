from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.base_context import BaseContext
from slack_bolt.context.respond.async_respond import AsyncRespond
from slack_bolt.context.say.async_say import AsyncSay


class AsyncBoltContext(BaseContext):
    """Context object associated with a request from Slack."""

    @property
    def client(self) -> Optional[AsyncWebClient]:
        """The `AsyncWebClient` instance available for this request.

            @app.event("app_mention")
            async def handle_events(context):
                await context.client.chat_postMessage(
                    channel=context.channel_id,
                    text="Thanks!",
                )

            # You can access "client" this way too.
            @app.event("app_mention")
            async def handle_events(client, context):
                await client.chat_postMessage(
                    channel=context.channel_id,
                    text="Thanks!",
                )

        Returns:
            `AsyncWebClient` instance
        """
        if "client" not in self:
            self["client"] = AsyncWebClient(token=None)
        return self["client"]

    @property
    def ack(self) -> AsyncAck:
        """`ack()` function for this request.

            @app.action("button")
            async def handle_button_clicks(context):
                await context.ack()

            # You can access "ack" this way too.
            @app.action("button")
            async def handle_button_clicks(ack):
                await ack()

        Returns:
            Callable `ack()` function
        """
        if "ack" not in self:
            self["ack"] = AsyncAck()
        return self["ack"]

    @property
    def say(self) -> AsyncSay:
        """`say()` function for this request.

            @app.action("button")
            async def handle_button_clicks(context):
                await context.ack()
                await context.say("Hi!")

            # You can access "ack" this way too.
            @app.action("button")
            async def handle_button_clicks(ack, say):
                await ack()
                await say("Hi!")

        Returns:
            Callable `say()` function
        """
        if "say" not in self:
            self["say"] = AsyncSay(client=self.client, channel=self.channel_id)
        return self["say"]

    @property
    def respond(self) -> Optional[AsyncRespond]:
        """`respond()` function for this request.

            @app.action("button")
            async def handle_button_clicks(context):
                await context.ack()
                await context.respond("Hi!")

            # You can access "ack" this way too.
            @app.action("button")
            async def handle_button_clicks(ack, respond):
                await ack()
                await respond("Hi!")

        Returns:
            Callable `respond()` function
        """
        if "respond" not in self:
            self["respond"] = AsyncRespond(response_url=self.response_url)
        return self["respond"]
