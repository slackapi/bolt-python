import re

from slack_bolt.adapter.bottle import SlackRequestHandler
from slack_bolt.app import App
from slack_bolt.oauth.oauth_settings import OAuthSettings

signing_secret = "secret"
app = App(
    signing_secret=signing_secret,
    oauth_settings=OAuthSettings(
        client_id="111.111", client_secret="xxx", scopes=["chat:write", "commands"],
    ),
)
handler = SlackRequestHandler(app)

from bottle import get, request, response
from boddle import boddle


@get("/slack/install")
def install():
    return handler.handle(request, response)


class TestBottle:
    def test_oauth(self):
        with boddle(method="GET", path="/slack/install"):
            response_body = install()
            assert response_body == ""
            assert response.status_code == 302
            assert re.match(
                "https://slack.com/oauth/v2/authorize\\?state=[^&]+&client_id=111.111&scope=chat:write,commands&user_scope=",
                response.headers["Location"],
            )
