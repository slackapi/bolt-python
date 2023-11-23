from slack_bolt.cli.get_hooks import hooks_payload


class TestGetHooks:
    def test_hooks_payload(self):
        hooks = hooks_payload["hooks"]

        assert "slack_bolt.cli.get_manifest" in hooks["get-manifest"]
        assert "slack_bolt.cli.start" in hooks["start"]

    def test_hooks_payload_config(self):
        config = hooks_payload["config"]

        assert config["sdk-managed-connection-enabled"] == True
        assert config["protocol-version"] == ["message-boundaries", "default"]
