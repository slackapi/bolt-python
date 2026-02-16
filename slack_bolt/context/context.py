from typing import Optional

from slack_sdk import WebClient

from slack_bolt.context.ack import Ack
from slack_bolt.context.base_context import BaseContext
from slack_bolt.context.complete import Complete
from slack_bolt.context.fail import Fail
from slack_bolt.context.get_thread_context.get_thread_context import GetThreadContext
from slack_bolt.context.respond import Respond
from slack_bolt.context.save_thread_context import SaveThreadContext
from slack_bolt.context.say import Say
from slack_bolt.context.set_status import SetStatus
from slack_bolt.context.set_suggested_prompts import SetSuggestedPrompts
from slack_bolt.context.set_title import SetTitle
from slack_bolt.util.utils import create_copy


class BoltContext(BaseContext):
    """Context object associated with a request from Slack."""

    def to_copyable(self) -> "BoltContext":
        new_dict = {}
        for prop_name, prop_value in self.items():
            if prop_name in self.copyable_standard_property_names:
                # all the standard properties are copiable
                new_dict[prop_name] = prop_value
            elif prop_name in self.non_copyable_standard_property_names:
                # Do nothing with this property (e.g., listener_runner)
                continue
            else:
                try:
                    copied_value = create_copy(prop_value)
                    new_dict[prop_name] = copied_value
                except TypeError as te:
                    self.logger.warning(
                        f"Skipped setting '{prop_name}' to a copied request for lazy listeners "
                        "due to a deep-copy creation error. Consider passing the value not as part of context object "
                        f"(error: {te})"
                    )
        return BoltContext(new_dict)

    # The return type is intentionally string to avoid circular imports
    @property
    def listener_runner(self) -> "ThreadListenerRunner":  # type: ignore[name-defined]
        """The properly configured listener_runner that is available for middleware/listeners."""
        return self["listener_runner"]

    @property
    def client(self) -> WebClient:
        """The `WebClient` instance available for this request.

            @app.event("app_mention")
            def handle_events(context):
                context.client.chat_postMessage(
                    channel=context.channel_id,
                    text="Thanks!",
                )

            # You can access "client" this way too.
            @app.event("app_mention")
            def handle_events(client, context):
                client.chat_postMessage(
                    channel=context.channel_id,
                    text="Thanks!",
                )

        Returns:
            `WebClient` instance
        """
        if "client" not in self:
            self["client"] = WebClient(token=None)
        return self["client"]

    @property
    def ack(self) -> Ack:
        """`ack()` function for this request.

            @app.action("button")
            def handle_button_clicks(context):
                context.ack()

            # You can access "ack" this way too.
            @app.action("button")
            def handle_button_clicks(ack):
                ack()

        Returns:
            Callable `ack()` function
        """
        if "ack" not in self:
            self["ack"] = Ack()
        return self["ack"]

    @property
    def say(self) -> Say:
        """`say()` function for this request.

            @app.action("button")
            def handle_button_clicks(context):
                context.ack()
                context.say("Hi!")

            # You can access "ack" this way too.
            @app.action("button")
            def handle_button_clicks(ack, say):
                ack()
                say("Hi!")

        Returns:
            Callable `say()` function
        """
        if "say" not in self:
            self["say"] = Say(client=self.client, channel=self.channel_id, thread_ts=self.thread_ts)
        return self["say"]

    @property
    def respond(self) -> Optional[Respond]:
        """`respond()` function for this request.

            @app.action("button")
            def handle_button_clicks(context):
                context.ack()
                context.respond("Hi!")

            # You can access "ack" this way too.
            @app.action("button")
            def handle_button_clicks(ack, respond):
                ack()
                respond("Hi!")

        Returns:
            Callable `respond()` function
        """
        if "respond" not in self:
            self["respond"] = Respond(
                response_url=self.response_url,
                proxy=self.client.proxy,
                ssl=self.client.ssl,
            )
        return self["respond"]

    @property
    def complete(self) -> Complete:
        """`complete()` function for this request. Once a custom function's state is set to complete,
        any outputs the function returns will be passed along to the next step of its housing workflow,
        or complete the workflow if the function is the last step in a workflow. Additionally,
        any interactivity handlers associated to a function invocation will no longer be invocable.

            @app.function("reverse")
            def handle_button_clicks(ack, complete):
                ack()
                complete(outputs={"stringReverse":"olleh"})

            @app.function("reverse")
            def handle_button_clicks(context):
                context.ack()
                context.complete(outputs={"stringReverse":"olleh"})

        Returns:
            Callable `complete()` function
        """
        if "complete" not in self:
            self["complete"] = Complete(client=self.client, function_execution_id=self.function_execution_id)
        return self["complete"]

    @property
    def fail(self) -> Fail:
        """`fail()` function for this request. Once a custom function's state is set to error,
        its housing workflow will be interrupted and any provided error message will be passed
        on to the end user through SlackBot. Additionally, any interactivity handlers associated
        to a function invocation will no longer be invocable.

            @app.function("reverse")
            def handle_button_clicks(ack, fail):
                ack()
                fail(error="something went wrong")

            @app.function("reverse")
            def handle_button_clicks(context):
                context.ack()
                context.fail(error="something went wrong")

        Returns:
            Callable `fail()` function
        """
        if "fail" not in self:
            self["fail"] = Fail(client=self.client, function_execution_id=self.function_execution_id)
        return self["fail"]

    @property
    def set_title(self) -> Optional[SetTitle]:
        return self.get("set_title")

    @property
    def set_status(self) -> Optional[SetStatus]:
        return self.get("set_status")

    @property
    def set_suggested_prompts(self) -> Optional[SetSuggestedPrompts]:
        return self.get("set_suggested_prompts")

    @property
    def get_thread_context(self) -> Optional[GetThreadContext]:
        return self.get("get_thread_context")

    @property
    def save_thread_context(self) -> Optional[SaveThreadContext]:
        return self.get("save_thread_context")
