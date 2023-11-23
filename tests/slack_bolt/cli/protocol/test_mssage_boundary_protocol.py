from slack_bolt.cli.protocol import MessageBoundaryProtocol


class TestMessageBoundaryProtocol:
    def test_name(self):
        assert MessageBoundaryProtocol.name == "message-boundaries"

    def test_debug(self, capsys, caplog):
        protocol = MessageBoundaryProtocol("bound")

        protocol.debug("test")

        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""
        assert "DEBUG test" in caplog.text

    def test_info(self, capsys, caplog):
        protocol = MessageBoundaryProtocol("bound")

        protocol.info("test")

        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""
        assert "INFO test" in caplog.text

    def test_warning(self, capsys, caplog):
        protocol = MessageBoundaryProtocol("bound")

        protocol.warning("test")

        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""
        assert "WARNING test" in caplog.text

    def test_error(self, capsys, caplog):
        protocol = MessageBoundaryProtocol("bound")

        protocol.error("test")

        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""
        assert "ERROR test" in caplog.text

    def test_respond(self, capsys, caplog):
        protocol = MessageBoundaryProtocol("bound")

        protocol.respond("test")

        out, err = capsys.readouterr()
        assert out == "boundtestbound\n"
        assert err == ""
        assert "" in caplog.text
