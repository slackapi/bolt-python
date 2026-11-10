# Testing your app

`slack_bolt.testing` lets you unit test listeners without connecting to Slack. It has two parts:

* `MockSlackServer`: a small local HTTP server that stands in for the Slack Web API and for `response_url`. It records every API call your app makes and every message posted with `respond()`, and answers with canned responses. `auth.test` is answered with a bot installation by default, and every other method returns `{"ok": true}` unless you set a response.
* `BoltTestClient` (and `AsyncBoltTestClient` for `AsyncApp`): builds signed requests for events, messages, slash commands, block actions, shortcuts and view submissions, sends them through your app, and returns what happened.

Requests go through the app's full middleware chain, including request verification, authorization and listener matching. The test client runs listeners (and lazy listeners) to completion before returning, so you can assert on their side effects right away, whatever `process_before_response` is set to.

```python
import pytest
from slack_bolt import App
from slack_bolt.testing import BoltTestClient, MockSlackServer


@pytest.fixture
def server():
    with MockSlackServer() as server:
        yield server


def create_app(client) -> App:
    app = App(client=client, signing_secret="test-secret")

    @app.command("/ticket")
    def open_ticket(ack, command, respond, client):
        ack(f"Creating a ticket for: {command['text']}")
        client.chat_postMessage(channel="C_SUPPORT", text=command["text"])
        respond("Your ticket was created")

    return app


def test_ticket_command(server):
    app = create_app(server.web_client())
    result = BoltTestClient(app, server).slash_command("/ticket", "printer is on fire")

    assert result.status == 200
    assert result.body == "Creating a ticket for: printer is on fire"
    assert result.calls_to("chat.postMessage")[0].args["channel"] == "C_SUPPORT"
    assert result.responds == [{"text": "Your ticket was created"}]
```

## Canned API responses

```python
server.set_response("users.info", {"ok": True, "user": {"id": "U123", "real_name": "Ada"}})
server.set_response("chat.postMessage", {"ok": False, "error": "channel_not_found"})
```

An `"ok": false` response raises `SlackApiError` in your listener, the same as the real API.

## Other request types

```python
tester = BoltTestClient(app, server)
tester.message("hello", user="U123", channel="C123")
tester.event({"type": "app_mention", "channel": "C123", "ts": "1.1", "text": "<@U0> hi"})
tester.block_action("approve_button", value="request-42")
tester.shortcut("open_form")
tester.message_shortcut("save_message", message={"type": "message", "text": "hi", "ts": "1.2"})
tester.view_submission("form", {"title_block": {"title": {"type": "plain_text_input", "value": "Hi"}}})
```

Each method returns a `DispatchResult` with `status`, `body`, `json` (the body parsed as JSON, for example `response_action` errors from a view submission), `api_calls`, `calls_to(method)` and `responds`. The payload builders are also available on their own in `slack_bolt.testing.payloads` if you want to customize a payload and send it with `tester.dispatch(payload)`.

## Apps created at import time

If your app is created at module level with a token from the environment, you can still test it: `BoltTestClient` points the app's Web API client at the mock server. Disable token verification so creating the app doesn't call Slack:

```python
app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"],
          token_verification_enabled=False)
```

## AsyncApp

```python
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.async_app import AsyncApp
from slack_bolt.testing.async_client import AsyncBoltTestClient


async def test_async_command(server):
    app = AsyncApp(client=AsyncWebClient(token="xoxb-test", base_url=server.base_url), signing_secret="test-secret")

    @app.command("/hello")
    async def hello(ack, respond):
        await ack()
        await respond("Hi!")

    result = await AsyncBoltTestClient(app, server).slash_command("/hello")
    assert result.responds == [{"text": "Hi!"}]
```
