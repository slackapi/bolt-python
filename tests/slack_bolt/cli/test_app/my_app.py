import os

from slack_sdk import WebClient
from slack_bolt.app import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from tests.slack_bolt.cli.utils import get_test_socket_mode_handler, wait_for_test_socket_connection

assert "SLACK_BOT_TOKEN" in os.environ
assert "SLACK_APP_TOKEN" in os.environ

if __name__ == "__main__":
    print(f"ran as __main__")

web_client = WebClient(
    token=os.environ["SLACK_BOT_TOKEN"],
    base_url="http://localhost:8888",
)

app = App(signing_secret="secret", client=web_client)

if __name__ == "__main__":
    print(f"ran as __main__")
    handler = get_test_socket_mode_handler(3012, app, os.environ.get("SLACK_APP_TOKEN"))
    handler.connect()
    wait_for_test_socket_connection(handler, 2)
