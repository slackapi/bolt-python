import os
import logging

from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)
app = App()


@app.command("/hello-bolt-python")
def hello(payload, ack):
    user_id = payload["user_id"]
    ack(f"Hi! <@{user_id}>")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
