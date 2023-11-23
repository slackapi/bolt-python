from slack_bolt.cli.protocol import DefaultProtocol


class TestDefaultProtocol:
    def test_name(self):
        assert DefaultProtocol.name == "default"

    def test_debug(self, capsys):
        DefaultProtocol().debug("test")

        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""

    def test_info(self, capsys):
        DefaultProtocol().info("test")

        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""

    def test_warning(self, capsys):
        DefaultProtocol().warning("test")

        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""

    def test_error(self, capsys):
        DefaultProtocol().error("test")

        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""

    def test_error(self, capsys):
        DefaultProtocol().respond("test")

        out, err = capsys.readouterr()
        assert out == "test\n"
        assert err == ""
