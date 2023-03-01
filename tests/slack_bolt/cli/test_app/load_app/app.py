import os

from slack_bolt.app import App
from slack_sdk import WebClient

signing_secret = "secret"
valid_token = "xoxb-valid"
mock_api_server_base_url = "http://localhost:8888"
web_client = WebClient(
    token=valid_token,
    base_url=mock_api_server_base_url,
)

app = App(signing_secret=signing_secret, client=web_client)

# Start Bolt app
if __name__ == "__main__":
    print(f"{os.path.basename(__file__)} ran")
