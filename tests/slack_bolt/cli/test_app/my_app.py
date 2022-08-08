import os

assert "SLACK_BOT_TOKEN" in os.environ
assert "SLACK_APP_TOKEN" in os.environ


# Start Bolt app
if __name__ == "__main__":
    print(f"{os.path.basename(__file__)} ran")
