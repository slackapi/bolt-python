import asyncio

import pytest

from slack_bolt.async_app import AsyncApp
from slack_bolt.testing import MockSlackServer
from slack_bolt.testing.async_client import AsyncBoltTestClient
from slack_sdk.web.async_client import AsyncWebClient


@pytest.fixture
def server():
    with MockSlackServer() as s:
        yield s


def build_app(server: MockSlackServer, **kwargs) -> AsyncApp:
    client = AsyncWebClient(token="xoxb-test", base_url=server.base_url)
    return AsyncApp(client=client, signing_secret="test-secret", **kwargs)


class TestAsyncBoltTestClient:
    @pytest.mark.asyncio
    async def test_slash_command_ack_and_respond(self, server: MockSlackServer):
        app = build_app(server)

        @app.command("/hello")
        async def hello(ack, command, respond):
            await ack("On it")
            await respond(f"Hi <@{command['user_id']}>!")

        result = await AsyncBoltTestClient(app, server).slash_command("/hello", user_id="U123")
        assert result.status == 200
        assert result.body == "On it"
        assert result.responds == [{"text": "Hi <@U123>!"}]

    @pytest.mark.asyncio
    async def test_waits_for_listener_tasks(self, server: MockSlackServer):
        app = build_app(server, process_before_response=False)

        @app.message("hello")
        async def greet(message, say):
            await asyncio.sleep(0.2)
            await say(f"Hey <@{message['user']}>")

        result = await AsyncBoltTestClient(app, server).message("hello", user="U9", channel="C9")
        post = result.calls_to("chat.postMessage")[0]
        assert (post.args["channel"], post.args["text"]) == ("C9", "Hey <@U9>")

    @pytest.mark.asyncio
    async def test_lazy_listeners(self, server: MockSlackServer):
        app = build_app(server, process_before_response=True)

        async def ack_fast(ack):
            await ack()

        async def do_work(respond):
            await asyncio.sleep(0.1)
            await respond("done")

        app.command("/work")(ack=ack_fast, lazy=[do_work])
        result = await AsyncBoltTestClient(app, server).slash_command("/work")
        assert result.responds == [{"text": "done"}]

    @pytest.mark.asyncio
    async def test_view_submission_errors(self, server: MockSlackServer):
        app = build_app(server)

        @app.view("reason")
        async def reason(ack):
            await ack(response_action="errors", errors={"reason": "Required"})

        result = await AsyncBoltTestClient(app, server).view_submission("reason")
        assert result.json == {"response_action": "errors", "errors": {"reason": "Required"}}

    @pytest.mark.asyncio
    async def test_timeout(self, server: MockSlackServer):
        app = build_app(server)

        @app.event("app_mention")
        async def forever():
            await asyncio.sleep(1)

        tester = AsyncBoltTestClient(app, server, timeout=0.2)
        with pytest.raises(asyncio.TimeoutError):
            await tester.event({"type": "app_mention", "channel": "C1", "ts": "1.1", "text": "hi"})
