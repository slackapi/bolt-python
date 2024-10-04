import json
import logging
import os
from typing import Set
import random
import time

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App, Assistant, SetStatus, Say, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    # This must be set to handle bot message events
    ignoring_self_assistant_message_events_enabled=False,
)


assistant = Assistant()
# You can use your own thread_context_store if you want
# from slack_bolt import FileAssistantThreadContextStore
# assistant = Assistant(thread_context_store=FileAssistantThreadContextStore())


@assistant.thread_started
def start_thread(say: Say):
    say(
        text=":wave: Hi, how can I help you today?",
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": ":wave: Hi, how can I help you today?"},
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "action_id": "assistant-generate-random-numbers",
                        "text": {"type": "plain_text", "text": "Generate random numbers"},
                        "value": "1",
                    },
                ],
            },
        ],
    )


@app.action("assistant-generate-random-numbers")
def configure_assistant_summarize_channel(ack: Ack, client: WebClient, body: dict):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "configure_assistant_summarize_channel",
            "title": {"type": "plain_text", "text": "My Assistant"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "private_metadata": json.dumps(
                {
                    "channel_id": body["channel"]["id"],
                    "thread_ts": body["message"]["thread_ts"],
                }
            ),
            "blocks": [
                {
                    "type": "input",
                    "block_id": "num",
                    "label": {"type": "plain_text", "text": "# of outputs"},
                    "element": {
                        "type": "static_select",
                        "action_id": "input",
                        "placeholder": {"type": "plain_text", "text": "How many numbers do you need?"},
                        "options": [
                            {"text": {"type": "plain_text", "text": "5"}, "value": "5"},
                            {"text": {"type": "plain_text", "text": "10"}, "value": "10"},
                            {"text": {"type": "plain_text", "text": "20"}, "value": "20"},
                        ],
                        "initial_option": {"text": {"type": "plain_text", "text": "5"}, "value": "5"},
                    },
                }
            ],
        },
    )


@app.view("configure_assistant_summarize_channel")
def receive_configure_assistant_summarize_channel(ack: Ack, client: WebClient, payload: dict):
    ack()
    num = payload["state"]["values"]["num"]["input"]["selected_option"]["value"]
    thread = json.loads(payload["private_metadata"])
    client.chat_postMessage(
        channel=thread["channel_id"],
        thread_ts=thread["thread_ts"],
        text=f"OK, you need {num} numbers. I will generate it shortly!",
        metadata={
            "event_type": "assistant-generate-random-numbers",
            "event_payload": {"num": int(num)},
        },
    )


@assistant.bot_message
def respond_to_bot_messages(logger: logging.Logger, set_status: SetStatus, say: Say, payload: dict):
    try:
        if payload.get("metadata", {}).get("event_type") == "assistant-generate-random-numbers":
            set_status("is generating an array of random numbers...")
            time.sleep(1)
            nums: Set[str] = set()
            num = payload["metadata"]["event_payload"]["num"]
            while len(nums) < num:
                nums.add(str(random.randint(1, 100)))
            say(f"Here you are: {', '.join(nums)}")
        else:
            # nothing to do for this bot message
            # If you want to add more patterns here, be careful not to cause infinite loop messaging
            pass

    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")


@assistant.user_message
def respond_to_user_messages(logger: logging.Logger, set_status: SetStatus, say: Say):
    try:
        set_status("is typing...")
        say("Sorry, I couldn't understand your comment. Could you say it in a different way?")
    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        say(f":warning: Sorry, something went wrong during processing your request (error: {e})")


app.use(assistant)


@app.event("message")
def handle_message_in_channels():
    pass  # noop


@app.event("app_mention")
def handle_non_assistant_thread_messages(say: Say):
    say(":wave: I can help you out within our 1:1 DM!")


if __name__ == "__main__":
    SocketModeHandler(app, app_token=os.environ["SLACK_APP_TOKEN"]).start()

# pip install slack_bolt
# export SLACK_APP_TOKEN=xapp-***
# export SLACK_BOT_TOKEN=xoxb-***
# python interaction_app.py
