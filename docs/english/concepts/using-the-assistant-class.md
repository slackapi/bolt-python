# Using the Assistant class

:::info[Some features within this guide require a paid plan]
If you don't have a paid workspace for development, you can join the [Developer Program](https://api.slack.com/developer-program) and provision a sandbox with access to all Slack features for free.
:::

The `Assistant` class can be used to handle the incoming events expected from a user interacting with an app in Slack that has the Agents & AI Apps feature enabled. 

A typical flow would look like:

1. [The user starts a thread](#handling-new-thread). The `Assistant` class handles the incoming [`assistant_thread_started`](/reference/events/assistant_thread_started) event.
2. [The thread context may change at any point](#handling-thread-context-changes). The `Assistant` class can handle any incoming [`assistant_thread_context_changed`](/reference/events/assistant_thread_context_changed) events. The class also provides a default `context` store to keep track of thread context changes as the user moves through Slack.
3. [The user responds](#handling-user-response). The `Assistant` class handles the incoming [`message.im`](/reference/events/message.im) event. 


```python
assistant = Assistant()

# This listener is invoked when a human user opened an assistant thread
@assistant.thread_started
def start_assistant_thread(
    say: Say,
    get_thread_context: GetThreadContext,
    set_suggested_prompts: SetSuggestedPrompts,
    logger: logging.Logger,
):
    try:
        ...

# This listener is invoked when the human user sends a reply in the assistant thread
@assistant.user_message
def respond_in_assistant_thread(
    client: WebClient,
    context: BoltContext,
    get_thread_context: GetThreadContext,
    logger: logging.Logger,
    payload: dict,
    say: Say,
    set_status: SetStatus,
):
    try:
        ...

# Enable this assistant middleware in your Bolt app
app.use(assistant)
```

:::info[Consider the following]
You _could_ go it alone and [listen](/tools/bolt-python/concepts/event-listening) for the `assistant_thread_started`, `assistant_thread_context_changed`, and `message.im` events in order to implement the AI features in your app. That being said, using the `Assistant` class will streamline the process. And we already wrote this nice guide for you!
:::

While the `assistant_thread_started` and `assistant_thread_context_changed` events do provide Slack-client thread context information, the `message.im` event does not. Any subsequent user message events won't contain thread context data. For that reason, Bolt not only provides a way to store thread context — the `threadContextStore` property — but it also provides a `DefaultThreadContextStore` instance that is utilized by default. This implementation relies on storing and retrieving [message metadata](/messaging/message-metadata/) as the user interacts with the app. 

If you do provide your own `threadContextStore` property, it must feature `get` and `save` methods.

:::tip[Refer to the [reference docs](https://docs.slack.dev/tools/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.]
:::

## Configuring your app to support the `Assistant` class {#configuring-assistant-class}

1. Within [App Settings](https://api.slack.com/apps), enable the **Agents & AI Apps** feature.

2. Within the App Settings **OAuth & Permissions** page, add the following scopes: 
  * [`assistant:write`](/reference/scopes/assistant.write)
  * [`chat:write`](/reference/scopes/chat.write)
  * [`im:history`](/reference/scopes/im.history)

3. Within the App Settings **Event Subscriptions** page, subscribe to the following events: 
  * [`assistant_thread_started`](/reference/events/assistant_thread_started)
  * [`assistant_thread_context_changed`](/reference/events/assistant_thread_context_changed)
  * [`message.im`](/reference/events/message.im)

## Handling a new thread {#handling-new-thread}

When the user opens a new thread with your AI-enabled app, the [`assistant_thread_started`](/reference/events/assistant_thread_started) event will be sent to your app.

:::tip[When a user opens an app thread while in a channel, the channel info is stored as the thread's `AssistantThreadContext` data.] 

You can grab that info by using the `get_thread_context` utility, as subsequent user message event payloads won't include the channel info.
:::

```python
assistant = Assistant()

@assistant.thread_started
def start_assistant_thread(
    say: Say,
    get_thread_context: GetThreadContext,
    set_suggested_prompts: SetSuggestedPrompts,
    logger: logging.Logger,
):
    try:
        say("How can I help you?")

        prompts: List[Dict[str, str]] = [
            {
                "title": "Suggest names for my Slack app",
                "message": "Can you suggest a few names for my Slack app? The app helps my teammates better organize information and plan priorities and action items.",
            },
        ]

        thread_context = get_thread_context()
        if thread_context is not None and thread_context.channel_id is not None:
            summarize_channel = {
                "title": "Summarize the referred channel",
                "message": "Can you generate a brief summary of the referred channel?",
            }
            prompts.append(summarize_channel)

        set_suggested_prompts(prompts=prompts)
    except Exception as e:
        logger.exception(f"Failed to handle an assistant_thread_started event: {e}", e)
        say(f":warning: Something went wrong! ({e})")
```

You can send more complex messages to the user — see [Sending Block Kit alongside messages](#block-kit-interactions) for more info. 

## Handling thread context changes {#handling-thread-context-changes}

When the user switches channels, the [`assistant_thread_context_changed`](/reference/events/assistant_thread_context_changed) event will be sent to your app. 

If you use the built-in `Assistant` middleware without any custom configuration, the updated context data is automatically saved as [message metadata](/messaging/message-metadata/) of the first reply from the app. 

As long as you use the built-in approach, you don't need to store the context data within a datastore. The downside of this default behavior is the overhead of additional calls to the Slack API. These calls include those to `conversations.history`, which are used to look up the stored message metadata that contains the thread context (via `get_thread_context`). 

To store context elsewhere, pass a custom `AssistantThreadContextStore` implementation to the `Assistant` constructor. We provide `FileAssistantThreadContextStore`, which is a reference implementation that uses the local file system. Since this reference implementation relies on local files, it's not advised for use in production. For production apps, we recommend creating a class that inherits `AssistantThreadContextStore`.

```python
from slack_bolt import FileAssistantThreadContextStore
assistant = Assistant(thread_context_store=FileAssistantThreadContextStore())
```

## Handling the user response {#handling-user-response}

When the user messages your app, the [`message.im`](/reference/events/message.im) event will be sent to your app.

Messages sent to the app do not contain a [subtype](/reference/events/message#subtypes) and must be deduced based on their shape and any provided [message metadata](/messaging/message-metadata/).

There are three utilities that are particularly useful in curating the user experience:
* [`say`](https://docs.slack.dev/tools/bolt-python/reference/#slack_bolt.Say)
* [`setTitle`](https://docs.slack.dev/tools/bolt-python/reference/#slack_bolt.SetTitle)
* [`setStatus`](https://docs.slack.dev/tools/bolt-python/reference/#slack_bolt.SetStatus)

Within the `setStatus` utility, you can cycle through strings passed into a `loading_messages` array.

```python
# This listener is invoked when the human user sends a reply in the assistant thread
@assistant.user_message
def respond_in_assistant_thread(
    client: WebClient,
    context: BoltContext,
    get_thread_context: GetThreadContext,
    logger: logging.Logger,
    payload: dict,
    say: Say,
    set_status: SetStatus,
):
    try:
        channel_id = payload["channel"]
        team_id = payload["team"]
        thread_ts = payload["thread_ts"]
        user_id = payload["user"]
        user_message = payload["text"]

        set_status(
            status="thinking...",
            loading_messages=[
                "Untangling the internet cables…",
                "Consulting the office goldfish…",
                "Convincing the AI to stop overthinking…",
            ],
        )

        # Collect the conversation history with this user
        replies = client.conversations_replies(
            channel=context.channel_id,
            ts=context.thread_ts,
            oldest=context.thread_ts,
            limit=10,
        )
        messages_in_thread: List[Dict[str, str]] = []
        for message in replies["messages"]:
            role = "user" if message.get("bot_id") is None else "assistant"
            messages_in_thread.append({"role": role, "content": message["text"]})

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

## Sending Block Kit alongside messages {#block-kit-interactions}

For advanced use cases, Block Kit buttons may be used instead of suggested prompts, as well as the sending of messages with structured [metadata](/messaging/message-metadata/) to trigger subsequent interactions with the user.

For example, an app can display a button such as "Summarize the referring channel" in the initial reply. When the user clicks the button and submits detailed information (such as the number of messages, days to check, purpose of the summary, etc.), the app can handle that information and post a message that describes the request with structured metadata.

By default, apps can't respond to their own bot messages (Bolt prevents infinite loops by default). However, if you pass `ignoring_self_assistant_message_events_enabled=False` to the `App` constructor and add a `bot_message` listener to your `Assistant` middleware, your app can continue processing the request as shown below:

```python
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    # This must be set to handle bot message events
    ignoring_self_assistant_message_events_enabled=False,
)

assistant = Assistant()

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
...
```

See the [_Creating agents: adding and handling feedback_](/tools/bolt-python/concepts/adding-agent-features#adding-and-handling-feedback) section for adding feedback buttons with Block Kit. 

Want to see the functionality described throughout this guide in action? We've created a [App Agent Template](https://github.com/slack-samples/bolt-python-assistant-template) repo for you to build from.