from slack_bolt import Ack, BoltResponse


class TestAck:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_text(self):
        ack = Ack()
        response: BoltResponse = ack(text="foo")
        assert (response.status, response.body) == (200, "foo")

    def test_blocks(self):
        ack = Ack()
        response: BoltResponse = ack(text="foo", blocks=[{"type": "divider"}])
        assert (response.status, response.body) == (
            200,
            '{"text": "foo", "blocks": [{"type": "divider"}]}',
        )

    def test_response_type(self):
        ack = Ack()
        response: BoltResponse = ack(text="foo", response_type="in_channel")
        assert (response.status, response.body) == (
            200,
            '{"text": "foo", "response_type": "in_channel"}',
        )

    def test_view_errors(self):
        ack = Ack()
        response: BoltResponse = ack(
            response_action="errors",
            errors={
                "block_title": "Title is required",
                "block_description": "Description must be longer than 10 characters",
            },
        )
        assert (response.status, response.body) == (
            200,
            '{"response_action": "errors", '
            '"errors": {'
            '"block_title": "Title is required", '
            '"block_description": "Description must be longer than 10 characters"'
            "}"
            "}",
        )

    def test_view_update(self):
        ack = Ack()
        response: BoltResponse = ack(
            response_action="update",
            view={
                "type": "modal",
                "callback_id": "view-id",
                "title": {"type": "plain_text", "text": "My App",},
                "close": {"type": "plain_text", "text": "Cancel",},
                "blocks": [{"type": "divider", "block_id": "b"}],
            },
        )
        assert (response.status, response.body) == (
            200,
            '{"response_action": "update", '
            '"view": {'
            '"type": "modal", '
            '"callback_id": "view-id", '
            '"title": {"type": "plain_text", "text": "My App"}, '
            '"close": {"type": "plain_text", "text": "Cancel"}, '
            '"blocks": [{"type": "divider", "block_id": "b"}]'
            "}"
            "}",
        )
