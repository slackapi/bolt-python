import os

from slack_bolt.app import App
from mocks import web_client_mock, signing_secret_mock

if __name__ == "__main__":
    print(f"ran as __main__")

app = App(signing_secret=signing_secret_mock, client=web_client_mock)
app2 = App(signing_secret=signing_secret_mock, client=web_client_mock)

# Start Bolt app
if __name__ == "__main__":
    print(f"{os.path.basename(__file__)} ran")
