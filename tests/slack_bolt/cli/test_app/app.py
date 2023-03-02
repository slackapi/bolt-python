import os

from slack_sdk import WebClient
from slack_bolt.app import App

assert "SLACK_BOT_TOKEN" in os.environ
assert "SLACK_APP_TOKEN" in os.environ

if __name__ == "__main__":
    print(f"ran as __main__")

web_client = WebClient(
    token=os.environ["SLACK_BOT_TOKEN"],
    base_url="http://localhost:8888",
)

app = App(signing_secret="valid", client=web_client)
