"""Utilities for testing Bolt apps without connecting to Slack.

`MockSlackServer` stands in for the Slack Web API and `response_url` endpoints and records
what your app sends to them. `BoltTestClient` sends signed requests (events, messages, slash
commands, actions, shortcuts and view submissions) to your app and returns what it did.

    from slack_bolt import App
    from slack_bolt.testing import BoltTestClient, MockSlackServer

    def test_hello_command():
        with MockSlackServer() as server:
            app = App(client=server.web_client(), signing_secret="test-secret")

            @app.command("/hello")
            def hello(ack, command, respond):
                ack()
                respond(f"Hi <@{command['user_id']}>!")

            result = BoltTestClient(app, server).slash_command("/hello")
            assert result.status == 200
            assert result.responds[0]["text"] == "Hi <@U0000000000>!"

For `AsyncApp`, use `slack_bolt.testing.async_client.AsyncBoltTestClient`.
"""

from . import payloads
from .mock_slack_server import APICall, MockSlackServer
from .client import BoltTestClient, DispatchResult, InlineExecutor

__all__ = [
    "APICall",
    "BoltTestClient",
    "DispatchResult",
    "InlineExecutor",
    "MockSlackServer",
    "payloads",
]
