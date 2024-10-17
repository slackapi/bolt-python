# flake8: noqa F811
import asyncio
import logging
import os
import random
import json

logging.basicConfig(level=logging.DEBUG)

from slack_bolt.async_app import AsyncApp, AsyncAssistant, AsyncSetStatus, AsyncSay, AsyncAck
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_sdk.web.async_client import AsyncWebClient

app = AsyncApp(
    token=os.environ["SLACK_BOT_TOKEN"],
    # This must be set to handle bot message events
    ignoring_self_assistant_message_events_enabled=False,
)


assistant = AsyncAssistant()
# You can use your own thread_context_store if you want
# from slack_bolt import FileAssistantThreadContextStore
# assistant = Assistant(thread_context_store=FileAssistantThreadContextStore())


@assistant.thread_started
async def start_thread(say: AsyncSay):
    await say(
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
async def configure_assistant_summarize_channel(ack: AsyncAck, client: AsyncWebClient, body: dict):
    await ack()
    await client.views_open(
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
async def receive_configure_assistant_summarize_channel(ack: AsyncAck, client: AsyncWebClient, payload: dict):
    await ack()
    num = payload["state"]["values"]["num"]["input"]["selected_option"]["value"]
    thread = json.loads(payload["private_metadata"])
    await client.chat_postMessage(
        channel=thread["channel_id"],
        thread_ts=thread["thread_ts"],
        text=f"OK, you need {num} numbers. I will generate it shortly!",
        metadata={
            "event_type": "assistant-generate-random-numbers",
            "event_payload": {"num": int(num)},
        },
    )


@assistant.bot_message
async def respond_to_bot_messages(logger: logging.Logger, set_status: AsyncSetStatus, say: AsyncSay, payload: dict):
    try:
        if payload.get("metadata", {}).get("event_type") == "assistant-generate-random-numbers":
            await set_status("is generating an array of random numbers...")
            await asyncio.sleep(1)
            nums: Set[str] = set()
            num = payload["metadata"]["event_payload"]["num"]
            while len(nums) < num:
                nums.add(str(random.randint(1, 100)))
            await say(f"Here you are: {', '.join(nums)}")
        else:
            # nothing to do for this bot message
            # If you want to add more patterns here, be careful not to cause infinite loop messaging
            pass

    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")


@assistant.user_message
async def respond_to_user_messages(logger: logging.Logger, set_status: AsyncSetStatus, say: AsyncSay):
    try:
        await set_status("is typing...")
        await say("Sorry, I couldn't understand your comment. Could you say it in a different way?")
    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        await say(f":warning: Sorry, something went wrong during processing your request (error: {e})")


app.use(assistant)


@app.event("message")
async def handle_message_in_channels():
    pass  # noop


@app.event("app_mention")
async def handle_non_assistant_thread_messages(say: AsyncSay):
    await say(":wave: I can help you out within our 1:1 DM!")


async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())

# pip install slack_bolt aiohttp
# export SLACK_APP_TOKEN=xapp-***
# export SLACK_BOT_TOKEN=xoxb-***
# python async_interaction_app.py
import asyncio
import json
import logging
import os
from typing import Set
import random

logging.basicConfig(level=logging.DEBUG)

from slack_bolt.async_app import AsyncApp, AsyncAssistant, AsyncSetStatus, AsyncSay, AsyncAck
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_sdk.web.async_client import AsyncWebClient

app = AsyncApp(
    token=os.environ["SLACK_BOT_TOKEN"],
    # This must be set to handle bot message events
    ignoring_self_assistant_message_events_enabled=False,
)


assistant = AsyncAssistant()
# You can use your own thread_context_store if you want
# from slack_bolt import FileAssistantThreadContextStore
# assistant = Assistant(thread_context_store=FileAssistantThreadContextStore())


@assistant.thread_started
async def start_thread(say: AsyncSay):
    await say(
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
async def configure_assistant_summarize_channel(ack: AsyncAck, client: AsyncWebClient, body: dict):
    await ack()
    await client.views_open(
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
async def receive_configure_assistant_summarize_channel(ack: AsyncAck, client: AsyncWebClient, payload: dict):
    await ack()
    num = payload["state"]["values"]["num"]["input"]["selected_option"]["value"]
    thread = json.loads(payload["private_metadata"])
    await client.chat_postMessage(
        channel=thread["channel_id"],
        thread_ts=thread["thread_ts"],
        text=f"OK, you need {num} numbers. I will generate it shortly!",
        metadata={
            "event_type": "assistant-generate-random-numbers",
            "event_payload": {"num": int(num)},
        },
    )


@assistant.bot_message
async def respond_to_bot_messages(logger: logging.Logger, set_status: AsyncSetStatus, say: AsyncSay, payload: dict):
    try:
        if payload.get("metadata", {}).get("event_type") == "assistant-generate-random-numbers":
            await set_status("is generating an array of random numbers...")
            await asyncio.sleep(1)
            nums: Set[str] = set()
            num = payload["metadata"]["event_payload"]["num"]
            while len(nums) < num:
                nums.add(str(random.randint(1, 100)))
            await say(f"Here you are: {', '.join(nums)}")
        else:
            # nothing to do for this bot message
            # If you want to add more patterns here, be careful not to cause infinite loop messaging
            pass

    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")


@assistant.user_message
async def respond_to_user_messages(logger: logging.Logger, set_status: AsyncSetStatus, say: AsyncSay):
    try:
        await set_status("is typing...")
        await say("Sorry, I couldn't understand your comment. Could you say it in a different way?")
    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        await say(f":warning: Sorry, something went wrong during processing your request (error: {e})")


app.use(assistant)


@app.event("message")
async def handle_message_in_channels():
    pass  # noop


@app.event("app_mention")
async def handle_non_assistant_thread_messages(say: AsyncSay):
    await say(":wave: I can help you out within our 1:1 DM!")


async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())

# pip install slack_bolt aiohttp
# export SLACK_APP_TOKEN=xapp-***
# export SLACK_BOT_TOKEN=xoxb-***
# python async_interaction_app.py
