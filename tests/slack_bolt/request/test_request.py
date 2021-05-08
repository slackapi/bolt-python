from slack_bolt.request.request import BoltRequest


class TestRequest:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_all_none_inputs_http(self):
        req = BoltRequest(body=None, headers=None, query=None, context=None)
        assert req is not None
        assert req.raw_body == ""
        assert req.body == {}

    def test_all_none_inputs_socket_mode(self):
        req = BoltRequest(
            body=None, headers=None, query=None, context=None, mode="socket_mode"
        )
        assert req is not None
        assert req.raw_body == ""
        assert req.body == {}
