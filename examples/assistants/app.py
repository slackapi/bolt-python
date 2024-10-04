import logging
import os
import time

from slack_bolt.context.get_thread_context.get_thread_context import GetThreadContext

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App, Assistant, SetStatus, SetTitle, SetSuggestedPrompts, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])


assistant = Assistant()
# You can use your own thread_context_store if you want
# from slack_bolt import FileAssistantThreadContextStore
# assistant = Assistant(thread_context_store=FileAssistantThreadContextStore())


@assistant.thread_started
def start_thread(say: Say, set_suggested_prompts: SetSuggestedPrompts):
    say(":wave: Hi, how can I help you today?")
    set_suggested_prompts(
        prompts=[
            "What does SLACK stand for?",
            "When Slack was released?",
        ]
    )


@assistant.user_message(matchers=[lambda payload: "help page" in payload["text"]])
def find_help_pages(
    payload: dict,
    logger: logging.Logger,
    set_title: SetTitle,
    set_status: SetStatus,
    say: Say,
):
    try:
        set_title(payload["text"])
        set_status("Searching help pages...")
        time.sleep(0.5)
        say("Please check this help page: https://www.example.com/help-page-123")
    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        say(f":warning: Sorry, something went wrong during processing your request (error: {e})")


@assistant.user_message
def answer_other_inquiries(
    payload: dict,
    logger: logging.Logger,
    set_title: SetTitle,
    set_status: SetStatus,
    say: Say,
    get_thread_context: GetThreadContext,
):
    try:
        set_title(payload["text"])
        set_status("Typing...")
        time.sleep(0.3)
        set_status("Still typing...")
        time.sleep(0.3)
        thread_context = get_thread_context()
        if thread_context is not None:
            channel = thread_context.channel_id
            say(f"Ah, you're referring to <#{channel}>! Do you need help with the channel?")
        else:
            say("Here you are! blah-blah-blah...")
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
# python app.py
