from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.base_context import BaseContext
from slack_bolt.context.respond.async_respond import AsyncRespond
from slack_bolt.context.say.async_say import AsyncSay
from slack_bolt.context.complete_error.async_complete_error import AsyncCompleteError
from slack_bolt.context.complete_success.async_complete_success import AsyncCompleteSuccess
from slack_bolt.util.utils import create_copy

CLIENT: str = "client"
ACK: str = "ack"
SAY: str = "say"
RESPOND: str = "respond"
COMPLETE_ERROR: str = "complete_error"
COMPLETE_SUCCESS: str = "complete_success"


class AsyncBoltContext(BaseContext):
    """Context object associated with a request from Slack."""

    def to_copyable(self) -> "AsyncBoltContext":
        new_dict = {}
        for prop_name, prop_value in self.items():
            if prop_name in self.standard_property_names:
                # all the standard properties are copiable
                new_dict[prop_name] = prop_value
            else:
                try:
                    copied_value = create_copy(prop_value)
                    new_dict[prop_name] = copied_value
                except TypeError as te:
                    self.logger.debug(
                        f"Skipped settings '{prop_name}' to a copied request for lazy listeners "
                        f"as it's not possible to make a deep copy (error: {te})"
                    )
        return AsyncBoltContext(new_dict)

    @property
    def client(self) -> Optional[AsyncWebClient]:
        f"""The `AsyncWebClient` instance available for this request.

            @app.event("app_mention")
            async def handle_events(context):
                await context.{CLIENT}.chat_postMessage(
                    channel=context.channel_id,
                    text="Thanks!",
                )

            # You can access "{CLIENT}" this way too.
            @app.event("app_mention")
            async def handle_events({CLIENT}, context):
                await {CLIENT}.chat_postMessage(
                    channel=context.channel_id,
                    text="Thanks!",
                )

        Returns:
            `AsyncWebClient` instance
        """
        if CLIENT not in self:
            self[CLIENT] = AsyncWebClient(token=None)
        return self[CLIENT]

    @property
    def ack(self) -> AsyncAck:
        f"""`{ACK}()` function for this request.

            @app.action("button")
            async def handle_button_clicks(context):
                await context.{ACK}()

            # You can access "{ACK}" this way too.
            @app.action("button")
            async def handle_button_clicks({ACK}):
                await {ACK}()

        Returns:
            Callable `{ACK}()` function
        """
        if ACK not in self:
            self[ACK] = AsyncAck()
        return self[ACK]

    @property
    def say(self) -> AsyncSay:
        f"""`{SAY}()` function for this request.

            @app.action("button")
            async def handle_button_clicks(context):
                await context.{ACK}()
                await context.{SAY}("Hi!")

            # You can access "{ACK}" this way too.
            @app.action("button")
            async def handle_button_clicks({ACK}, {SAY}):
                await {ACK}()
                await {SAY}("Hi!")

        Returns:
            Callable `{SAY}()` function
        """
        if SAY not in self:
            self[SAY] = AsyncSay(client=self.client, channel=self.channel_id)
        return self[SAY]

    @property
    def respond(self) -> Optional[AsyncRespond]:
        f"""`{RESPOND}()` function for this request.

            @app.action("button")
            async def handle_button_clicks(context):
                await context.{ACK}()
                await context.{RESPOND}("Hi!")

            # You can access "{ACK}" this way too.
            @app.action("button")
            async def handle_button_clicks({ACK}, {RESPOND}):
                await {ACK}()
                await {RESPOND}("Hi!")

        Returns:
            Callable `{RESPOND}()` function
        """
        if RESPOND not in self:
            self[RESPOND] = AsyncRespond(
                response_url=self.response_url,
                proxy=self.client.proxy,
                ssl=self.client.ssl,
            )
        return self[RESPOND]

    @property
    def complete_success(self) -> AsyncCompleteSuccess:
        f"""`{COMPLETE_SUCCESS}()` function for this request.

            @app.function("reverse")
            async def handle_button_clicks(context):
                await context.{COMPLETE_SUCCESS}({{"stringReverse":"olleh"}})

            @app.function("reverse")
            async def handle_button_clicks({COMPLETE_SUCCESS}):
                await {COMPLETE_SUCCESS}({{"stringReverse":"olleh"}})

        Returns:
            Callable `{COMPLETE_SUCCESS}()` function
        """
        if COMPLETE_SUCCESS not in self:
            self[COMPLETE_SUCCESS] = AsyncCompleteSuccess(
                client=self.client, function_execution_id=self.function_execution_id
            )
        return self[COMPLETE_SUCCESS]

    @property
    def complete_error(self) -> AsyncCompleteError:
        f"""`{COMPLETE_ERROR}()` function for this request.

            @app.function("reverse")
            async def handle_button_clicks(context):
                await context.{COMPLETE_ERROR}("an error spawned")

            @app.function("reverse")
            async def handle_button_clicks({COMPLETE_ERROR}):
                await {COMPLETE_ERROR}("an error spawned")

        Returns:
            Callable `{COMPLETE_ERROR}()` function
        """
        if COMPLETE_ERROR not in self:
            self[COMPLETE_ERROR] = AsyncCompleteError(client=self.client, function_execution_id=self.function_execution_id)
        return self[COMPLETE_ERROR]
