---
title: Agents & Assistants
lang: en
slug: /concepts/assistant
---

This guide page focuses on how to implement Agents & Assistants using Bolt framework. For general information about the feature, please refer to [this document page](https://api.slack.com/docs/apps/ai).

To get started, you'll need to enable the **Agents & Assistants** feature on [the app configuration page](https://api.slack.com/apps). Then, add [assistant:write](https://api.slack.com/scopes/assistant:write), [chat:write](https://api.slack.com/scopes/chat:write), and [im:history](https://api.slack.com/scopes/im:history) to the **bot** scopes on the **OAuth & Permissions** page. Also, make sure to subscribe to [assistant_thread_started](https://api.slack.com/events/assistant_thread_started), [assistant_thread_context_changed](https://api.slack.com/events/assistant_thread_context_changed), and [message.im](https://api.slack.com/events/message.im) events on the **Event Subscriptions** page.

Please note that this feature requires a paid plan. If you don't have a paid workspace for development, you can join the [Developer Program](https://api.slack.com/developer-program) and provision a sandbox with access to all Slack features for free.

To handle assistant thread interactions with humans, although you can implement your agents using `app.event(...)` listeners for `assistant_thread_started`, `assistant_thread_context_changed`, and `message` events, Bolt offers a simpler approach. You just need to create an `Assistant` instance, attach the needed event handlers to it, and then add the assistant to your `App` instance.

```python
assistant = Assistant()

# This listener is invoked when a human user opened an assistant thread
@assistant.thread_started
def start_assistant_thread(say: Say, set_suggested_prompts: SetSuggestedPrompts):
    # Send the first reply to the human who started chat with your app's assistant bot
    say(":wave: Hi, how can I help you today?")

    # Setting suggested prompts is optional
    set_suggested_prompts(
        prompts=[
            # If the suggested prompt is long, you can use {"title": "short one to display", "message": "full prompt"} instead
            "What does SLACK stand for?",
            "When Slack was released?",
        ],
    )

# This listener is invoked when the human user sends a rely in the assistant thread
@assistant.user_message
def respond_in_assistant_thread(
    payload: dict,
    logger: logging.Logger,
    context: BoltContext,
    set_status: SetStatus,
    say: Say,
):
    try:
        # Tell the human user the assistant bot acknowledges the request and is working on it
        set_status("is typing...")

        # Collect the conversation history with this user
        replies_in_thread = client.conversations_replies(
            channel=context.channel_id,
            ts=context.thread_ts,
            oldest=context.thread_ts,
            limit=10,
        )
        messages_in_thread: List[Dict[str, str]] = []
        for message in replies_in_thread["messages"]:
            role = "user" if message.get("bot_id") is None else "assistant"
            messages_in_thread.append({"role": role, "content": message["text"]})

        # Pass the latest prompt and chat history to the LLM (call_llm is your own code)
        returned_message = call_llm(messages_in_thread)

        # Post the result in the assistant thread
        say(text=returned_message)

    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        # Don't forget sending a message telling the error
        # Without this, the status 'is typing...' won't be cleared, therefore the end-user is unable to continue the chat
        say(f":warning: Sorry, something went wrong during processing your request (error: {e})")

# Enable this assistant middleware in your Bolt app
app.use(assistant)
```

Refer to [the module document](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.

When an end-user opens an assistant thread next to a channel, the channel information is stored as the thread's `AssistantThreadContext` data, and you can access this information by using `get_thread_context` utility.

When the user switches the channel, the `assistant_thread_context_changed` event will be sent to your app. If you use the built-in `Assistant` middleware without any custom configuration (like the above code snippet does), the updated context data is automatically saved as message metadata of the first reply from the assistant bot. This means that, as long as you go with this built-in approach, you don't need to store the context data within any datastore. The only downside of this default module is the runtime overhead of additional Slack API calls. More specifically, it calls `conversations.history` API to look up the stored message metadata when you execute `get_thread_context`.

If you prefer storing this data elsewhere, you can pass your own `AssistantThreadContextStore` implementation to the `Assistant` constructor. We provide a reference implementation using the local file system, named `FileAssistantThreadContextStore`:

```python
# You can use your own thread_context_store if you want
from slack_bolt import FileAssistantThreadContextStore
assistant = Assistant(thread_context_store=FileAssistantThreadContextStore())
```

Since this reference implementation relies on local files, it's not recommended for production-grade operations. For your production apps, please create your own class that inherits `AssistantThreadContextStore`.

<details>

<summary>
Block Kit interactions in the assistant thread
</summary>

For advanced use cases, you might want to use Block Kit buttons instead of the suggested prompts. Additionally, consider sending a message with structured metadata to trigger subsequent interactions with the user.

For example, your app can display a button like "Summarize the referring channel" in the initial reply. When an end-user clicks the button and submits detailed information (such as the number of messages, days to check, the purpose of the summary, etc.), your app can handle the received information and post a bot message describing the request with structured metadata.

By default, your app can't respond to its own bot messages (Bolt prevents infinite loops by default). However, if you pass `ignoring_self_assistant_message_events_enabled=False` to the `App` constructor and add a `bot_message` listener to your `Assistant` middleware, your app can continue processing the request as shown below:

```python
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    # This must be set to handle bot message events
    ignoring_self_assistant_message_events_enabled=False,
)

assistant = Assistant()

# Refer to https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html to learn available listener arguments

@assistant.thread_started
def start_assistant_thread(say: Say):
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
                    # You can have multiple buttons here
                    {
                        "type": "button",
                        "action_id": "assistant-generate-random-numbers",
                        "text": {"type": "plain_text", "text": "Generate random numbers"},
                        "value": "clicked",
                    },
                ],
            },
        ],
    )

# This listener is invoked when the above button is clicked
@app.action("assistant-generate-random-numbers")
def configure_random_number_generation(ack: Ack, client: WebClient, body: dict):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "configure_assistant_summarize_channel",
            "title": {"type": "plain_text", "text": "My Assistant"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            # Relay the assistant thread information to app.view listener
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
                    # You can have this kind of predefined input from a user instead of parsing human text
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

# This listener is invoked when the above modal is submitted
@app.view("configure_assistant_summarize_channel")
def receive_random_number_generation_details(ack: Ack, client: WebClient, payload: dict):
    ack()
    num = payload["state"]["values"]["num"]["input"]["selected_option"]["value"]
    thread = json.loads(payload["private_metadata"])

    # Post a bot message with structured input data
    # The following assistant.bot_message will continue processing
    # If you prefer processing this request within this listener, it also works!
    # If you don't need bot_message listener, no need to set ignoring_self_assistant_message_events_enabled=False
    client.chat_postMessage(
        channel=thread["channel_id"],
        thread_ts=thread["thread_ts"],
        text=f"OK, you need {num} numbers. I will generate it shortly!",
        metadata={
            "event_type": "assistant-generate-random-numbers",
            "event_payload": {"num": int(num)},
        },
    )

# This listener is invoked whenever your app's bot user posts a message
@assistant.bot_message
def respond_to_bot_messages(logger: logging.Logger, set_status: SetStatus, say: Say, payload: dict):
    try:
        if payload.get("metadata", {}).get("event_type") == "assistant-generate-random-numbers":
            # Handle the above random-number-generation request
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

# This listener is invoked when the human user posts a reply
@assistant.user_message
def respond_to_user_messages(logger: logging.Logger, set_status: SetStatus, say: Say):
    try:
        set_status("is typing...")
        say("Please use the buttons in the first reply instead :bow:")
    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        say(f":warning: Sorry, something went wrong during processing your request (error: {e})")


# Enable this assistant middleware in your Bolt app
app.use(assistant)
```

</details>


Lastly, if you want to check full working example app, you can check [our sample repository](https://github.com/slack-samples/bolt-python-assistant-template) on GitHub.