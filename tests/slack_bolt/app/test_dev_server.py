from slack_bolt.app.app import SlackAppDevelopmentServer, App


class TestDevServer:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_instance(self):
        server = SlackAppDevelopmentServer(
            port=3001,
            path="/slack/events",
            app=App(signing_secret="valid", token="xoxb-valid",),
        )
        assert server is not None
