import json
import time

import pytest
from slack_sdk import WebClient

from slack_bolt import App
from slack_bolt.testing import BoltTestClient, MockSlackServer, payloads


@pytest.fixture
def server():
    with MockSlackServer() as s:
        yield s


def build_app(server: MockSlackServer, **kwargs) -> App:
    return App(client=server.web_client("xoxb-test"), signing_secret="test-secret", **kwargs)


class TestMockSlackServer:
    def test_records_calls_and_returns_canned_responses(self, server: MockSlackServer):
        client = server.web_client("xoxb-abc")
        auth = client.auth_test()
        assert auth["user_id"] == server.bot_user_id
        assert auth["team_id"] == server.team_id

        server.set_response("conversations.info", {"ok": True, "channel": {"id": "C1", "name": "general"}})
        assert client.conversations_info(channel="C1")["channel"]["name"] == "general"

        client.chat_postMessage(channel="C1", text="hello", blocks=[{"type": "divider"}])
        call = server.calls_to("chat.postMessage")[0]
        assert call.args["channel"] == "C1"
        assert call.args["text"] == "hello"
        assert call.token == "xoxb-abc"
        assert [c.method for c in server.calls] == ["auth.test", "conversations.info", "chat.postMessage"]

        server.reset()
        assert server.calls == []

    def test_error_responses_raise_like_slack(self, server: MockSlackServer):
        from slack_sdk.errors import SlackApiError

        server.set_response("chat.postMessage", {"ok": False, "error": "channel_not_found"})
        with pytest.raises(SlackApiError) as e:
            server.web_client().chat_postMessage(channel="C404", text="hi")
        assert e.value.response["error"] == "channel_not_found"

    def test_requires_start(self):
        with pytest.raises(RuntimeError):
            MockSlackServer().base_url


class TestBoltTestClient:
    def test_slash_command_ack_and_respond(self, server: MockSlackServer):
        app = build_app(server)

        @app.command("/hello")
        def hello(ack, command, respond):
            ack(f"Working on {command['text']}...")
            respond(text=f"Hi <@{command['user_id']}>!", response_type="in_channel")

        result = BoltTestClient(app, server).slash_command("/hello", "the report", user_id="U123")
        assert result.status == 200
        assert result.body == "Working on the report..."
        assert result.responds == [{"text": "Hi <@U123>!", "response_type": "in_channel"}]

    def test_message_event_and_say(self, server: MockSlackServer):
        app = build_app(server)

        @app.message("hello")
        def greet(message, say):
            say(f"Hey there <@{message['user']}>!")

        result = BoltTestClient(app, server).message("hello bot", user="U456", channel="C789")
        assert result.status == 200
        posts = result.calls_to("chat.postMessage")
        assert len(posts) == 1
        assert posts[0].args["channel"] == "C789"
        assert posts[0].args["text"] == "Hey there <@U456>!"

    def test_waits_for_listeners_without_process_before_response(self, server: MockSlackServer):
        app = build_app(server, process_before_response=False)

        @app.event("app_mention")
        def slow(event, client):
            time.sleep(0.2)
            client.reactions_add(channel=event["channel"], timestamp=event["ts"], name="eyes")

        result = BoltTestClient(app, server).event({"type": "app_mention", "channel": "C1", "ts": "1.1", "text": "hi"})
        assert [c.method for c in result.api_calls] == ["reactions.add"]

    def test_lazy_listeners_run_before_returning(self, server: MockSlackServer):
        app = build_app(server, process_before_response=True)

        def ack_fast(ack):
            ack()

        def do_work(respond):
            respond("done")

        app.command("/work")(ack=ack_fast, lazy=[do_work])

        result = BoltTestClient(app, server).slash_command("/work")
        assert result.status == 200
        assert result.responds == [{"text": "done"}]

    def test_block_action_and_view_submission(self, server: MockSlackServer):
        app = build_app(server)

        @app.action("approve")
        def approve(ack, body, client):
            ack()
            client.views_open(trigger_id=body["trigger_id"], view={"type": "modal", "callback_id": "reason"})

        @app.view("reason")
        def reason(ack, view):
            value = view["state"]["values"]["reason"]["input"]["value"]
            if not value:
                ack(response_action="errors", errors={"reason": "Required"})
            else:
                ack()

        tester = BoltTestClient(app, server)
        result = tester.block_action("approve", value="42")
        assert result.status == 200
        assert result.calls_to("views.open")[0].args["trigger_id"] == "111.222.test"

        values = {"reason": {"input": {"type": "plain_text_input", "value": ""}}}
        result = tester.view_submission("reason", values)
        assert result.json == {"response_action": "errors", "errors": {"reason": "Required"}}

        values["reason"]["input"]["value"] = "looks good"
        assert tester.view_submission("reason", values).body == ""

    def test_shortcuts(self, server: MockSlackServer):
        app = build_app(server)
        seen = []

        @app.shortcut("global_sc")
        def global_sc(ack, shortcut):
            ack()
            seen.append(shortcut["type"])

        @app.shortcut("message_sc")
        def message_sc(ack, shortcut, respond):
            ack()
            respond(f"Got {shortcut['message']['text']}")

        tester = BoltTestClient(app, server)
        assert tester.shortcut("global_sc").status == 200
        result = tester.message_shortcut("message_sc", message={"type": "message", "text": "hi", "ts": "1.2"})
        assert result.responds == [{"text": "Got hi"}]
        assert seen == ["shortcut"]

    def test_unhandled_and_invalid_requests(self, server: MockSlackServer):
        app = build_app(server)
        tester = BoltTestClient(app, server)
        assert tester.slash_command("/nobody-listens").status == 404

        tester.signing_secret = "wrong-secret"
        assert tester.slash_command("/nobody-listens").status == 401

    def test_listener_errors_return_500(self, server: MockSlackServer):
        app = build_app(server)

        @app.command("/boom")
        def boom(ack):
            raise ValueError("boom")

        assert BoltTestClient(app, server).slash_command("/boom").status == 500

    def test_redirects_an_app_built_with_a_default_client(self, server: MockSlackServer):
        # e.g. an app created at import time with a token from the environment
        app = App(token="xoxb-env", signing_secret="test-secret", token_verification_enabled=False)

        @app.event("app_home_opened")
        def home(event, client):
            client.views_publish(user_id=event["user"], view={"type": "home", "blocks": []})

        result = BoltTestClient(app, server).event({"type": "app_home_opened", "user": "U1", "tab": "home"})
        call = result.calls_to("views.publish")[0]
        assert call.args["user_id"] == "U1"
        assert call.token == "xoxb-env"


class TestPayloads:
    def test_http_encoding(self):
        assert payloads.to_http_body(payloads.slash_command("/a", "b")).startswith("token=")
        assert json.loads(payloads.to_http_body(payloads.message("hi")))["event"]["text"] == "hi"
        body = payloads.to_http_body(payloads.shortcut("x"))
        assert body.startswith("payload=")

    def test_signed_headers_verify(self):
        from slack_sdk.signature import SignatureVerifier

        body = payloads.to_http_body(payloads.message("hi"))
        headers = payloads.signed_headers(body, "secret")
        assert SignatureVerifier("secret").is_valid_request(body, headers)
        assert headers["content-type"] == "application/json"
