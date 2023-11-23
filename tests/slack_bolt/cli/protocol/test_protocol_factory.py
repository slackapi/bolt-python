from slack_bolt.cli.protocol import protocol_factory, DefaultProtocol, MessageBoundaryProtocol


class TestProtocolFactory:
    def test_default(self):
        args = []
        protocol = protocol_factory(args)
        assert isinstance(protocol, DefaultProtocol)

    def test_message_boundaries(self):
        args = [f"--protocol={MessageBoundaryProtocol.name}", "--bound=boundary"]
        protocol = protocol_factory(args)
        assert isinstance(protocol, MessageBoundaryProtocol)
