import logging
import os
import asyncio

from slack_bolt.context.get_thread_context.async_get_thread_context import AsyncGetThreadContext

logging.basicConfig(level=logging.DEBUG)

from slack_bolt.async_app import AsyncApp, AsyncAssistant, AsyncSetTitle, AsyncSetStatus, AsyncSetSuggestedPrompts, AsyncSay
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])


assistant = AsyncAssistant()


@assistant.thread_started
async def start_thread(say: AsyncSay, set_suggested_prompts: AsyncSetSuggestedPrompts):
    await say(":wave: Hi, how can I help you today?")
    await set_suggested_prompts(
        prompts=[
            "What does SLACK stand for?",
            "When Slack was released?",
        ]
    )


@assistant.user_message(matchers=[lambda body: "help page" in body["event"]["text"]])
async def find_help_pages(
    payload: dict,
    logger: logging.Logger,
    set_title: AsyncSetTitle,
    set_status: AsyncSetStatus,
    say: AsyncSay,
):
    try:
        await set_title(payload["text"])
        await set_status("Searching help pages...")
        await asyncio.sleep(0.5)
        await say("Please check this help page: https://www.example.com/help-page-123")
    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        await say(f":warning: Sorry, something went wrong during processing your request (error: {e})")


@assistant.user_message
async def answer_other_inquiries(
    payload: dict,
    logger: logging.Logger,
    set_title: AsyncSetTitle,
    set_status: AsyncSetStatus,
    say: AsyncSay,
    get_thread_context: AsyncGetThreadContext,
):
    try:
        await set_title(payload["text"])
        await set_status("Typing...")
        await asyncio.sleep(0.3)
        await set_status("Still typing...")
        await asyncio.sleep(0.3)
        thread_context = await get_thread_context()
        if thread_context is not None:
            channel = thread_context.channel_id
            await say(f"Ah, you're referring to <#{channel}>! Do you need help with the channel?")
        else:
            await say("Here you are! blah-blah-blah...")
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
# python async_app.py
