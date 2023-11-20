import os

from slack_sdk import WebClient
from slack_bolt.app import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

assert "SLACK_BOT_TOKEN" in os.environ
assert "SLACK_APP_TOKEN" in os.environ

if __name__ == "__main__":
    print(f"ran as __main__")

web_client = WebClient(
    base_url="http://localhost:8888",
)

app = App(signing_secret="valid", client=web_client)

SocketModeHandler(app).start()
