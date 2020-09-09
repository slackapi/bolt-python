from slack_sdk.models.blocks import DividerBlock

from slack_bolt.context.respond.internals import _build_message


class TestRespondInternals:
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_build_message_empty(self):
        message = _build_message()
        assert message is not None

    def test_build_message_text(self):
        message = _build_message(text="Hello!")
        assert message is not None

    def test_build_message_blocks(self):
        message = _build_message(blocks=[{"type": "divider"}])
        assert message is not None

    def test_build_message_blocks2(self):
        message = _build_message(blocks=[DividerBlock(block_id="foo")])
        assert message is not None
        assert isinstance(message["blocks"][0], dict)
        assert message["blocks"][0]["block_id"] == "foo"
