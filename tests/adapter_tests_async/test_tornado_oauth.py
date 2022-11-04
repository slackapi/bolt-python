from tornado.httpclient import HTTPRequest, HTTPResponse, HTTPClientError
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application

from slack_bolt.adapter.tornado.async_handler import AsyncSlackOAuthHandler
from slack_bolt.async_app import AsyncApp
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from tests.utils import remove_os_env_temporarily, restore_os_env

signing_secret = "secret"

app = AsyncApp(
    signing_secret=signing_secret,
    oauth_settings=AsyncOAuthSettings(
        client_id="111.111",
        client_secret="xxx",
        scopes=["chat:write", "commands"],
    ),
)


class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return Application([("/slack/install", AsyncSlackOAuthHandler, dict(app=app))])

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        self.old_os_env = remove_os_env_temporarily()

    def tearDown(self):
        AsyncHTTPTestCase.tearDown(self)
        restore_os_env(self.old_os_env)

    @gen_test
    async def test_oauth(self):
        request = HTTPRequest(url=self.get_url("/slack/install"), method="GET", follow_redirects=False)
        try:
            response: HTTPResponse = await self.http_client.fetch(request)
            assert response.code == 200
        except HTTPClientError as e:
            assert e.code == 200
