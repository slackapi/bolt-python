from typing import Optional

from slack_sdk.web.async_client import AsyncWebClient

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.base_context import BaseContext
from slack_bolt.context.complete.async_complete import AsyncComplete
from slack_bolt.context.fail.async_fail import AsyncFail
from slack_bolt.context.respond.async_respond import AsyncRespond
from slack_bolt.context.say.async_say import AsyncSay
from slack_bolt.util.utils import create_copy


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
            self["respond"] = AsyncRespond(
                response_url=self.response_url,
                proxy=self.client.proxy,
                ssl=self.client.ssl,
            )
        return self["respond"]

    @property
    def complete(self) -> AsyncComplete:
        """`complete()` function for this request. Once a custom function's state is set to complete,
        any outputs the function returns will be passed along to the next step of its housing workflow,
        or complete the workflow if the function is the last step in a workflow. Additionally,
        any interactivity handlers associated to a function invocation will no longer be invocable.

            @app.function("reverse")
            async def handle_button_clicks(ack, complete):
                await ack()
                await complete(outputs={"stringReverse":"olleh"})

            @app.function("reverse")
            async def handle_button_clicks(context):
                await context.ack()
                await context.complete(outputs={"stringReverse":"olleh"})

        Returns:
            Callable `complete()` function
        """
        if "complete" not in self:
            self["complete"] = AsyncComplete(client=self.client, function_execution_id=self.function_execution_id)
        return self["complete"]

    @property
    def fail(self) -> AsyncFail:
        """`fail()` function for this request. Once a custom function's state is set to error,
        its housing workflow will be interrupted and any provided error message will be passed
        on to the end user through SlackBot. Additionally, any interactivity handlers associated
        to a function invocation will no longer be invocable.

            @app.function("reverse")
            async def handle_button_clicks(ack, fail):
                await ack()
                await fail(error="something went wrong")

            @app.function("reverse")
            async def handle_button_clicks(context):
                await context.ack()
                await context.fail(error="something went wrong")

        Returns:
            Callable `fail()` function
        """
        if "fail" not in self:
            self["fail"] = AsyncFail(client=self.client, function_execution_id=self.function_execution_id)
        return self["fail"]
