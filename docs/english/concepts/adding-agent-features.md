---
sidebar_label: Adding agent features
---

# Adding agent features with Bolt for Python

:::tip[Check out the Support Agent sample app]
The code snippets throughout this guide are from our [Support Agent sample app](https://github.com/slack-samples/bolt-python-support-agent), Casey, which supports integration with Pydantic, Anthropic, and OpenAI. 

View our [agent quickstart](/ai/agent-quickstart) to get up and running with Casey. Otherwise, read on for exploration and explanation of agent-focused Bolt features found within Casey.
:::

Your agent can utilize features applicable to messages throughout Slack, like [chat streaming](#text-streaming) and [feedback buttons](#adding-and-handling-feedback). They can also [utilize the `Assistant` class](/tools/bolt-python/concepts/assistant-class) for a side-panel view designed with AI in mind.

If you're unfamiliar with using these feature within Slack, you may want to read the [API docs on the subject](/ai/). Then come back here to implement them with Bolt!

---

## Slack MCP Server {#slack-mcp-server}

Casey can harness the [Slack MCP Server](https://docs.slack.dev/ai/slack-mcp-server/developing) when deployed via an HTTP Server with OAuth. 

To enable the Slack MCP Server:

1. Install [ngrok](https://ngrok.com/download) and start a tunnel:

```sh
ngrok http 3000
```

2. Copy the `https://*.ngrok-free.app` URL from the ngrok output.

3. Update `manifest.json` for HTTP mode:
   - Set `socket_mode_enabled` to `false`
   - Replace `ngrok-free.app` with your ngrok domain (e.g. `YOUR_NGROK_SUBDOMAIN.ngrok-free.app`)

4. Create a new local dev app:

```sh
slack install -E local
```

5. Enable MCP for your app:
   - Run `slack app settings` to open your app's settings
   - Navigate to **Agents & AI Apps** in the left-side navigation
   - Toggle **Model Context Protocol** on

6. Update your `.env` OAuth environment variables:
   - Run `slack app settings` to open App Settings
   - Copy **Client ID**, **Client Secret**, and **Signing Secret**
   - Update `SLACK_REDIRECT_URI` in `.env` with your ngrok domain

```sh
SLACK_CLIENT_ID=YOUR_CLIENT_ID
SLACK_CLIENT_SECRET=YOUR_CLIENT_SECRET
SLACK_REDIRECT_URI=https://YOUR_NGROK_SUBDOMAIN.ngrok-free.app/slack/oauth_redirect
SLACK_SIGNING_SECRET=YOUR_SIGNING_SECRET
```

7. Start the app:

```sh
slack run app_oauth.py
```

8. Click the install URL printed in the terminal to install the app to your workspace via OAuth.

Your agent can now access the Slack MCP server!

---

## Listening for user invocation 

Agents can be invoked throughout Slack, such as via @mentions in channels, messaging the agent, and using the assistant side panel. 

<Tabs>
<TabItem value="appmention" label = "App mention">

```python
import re
from logging import Logger

from agents import Runner
from slack_bolt import BoltContext, Say, SayStream, SetStatus
from slack_sdk import WebClient

from agent import CaseyDeps, casey_agent
from thread_context import conversation_store
from listeners.views.feedback_builder import build_feedback_blocks


def handle_app_mentioned(
    client: WebClient,
    context: BoltContext,
    event: dict,
    logger: Logger,
    say: Say,
    say_stream: SayStream,
    set_status: SetStatus,
):
    """Handle @Casey mentions in channels."""
    try:
        channel_id = context.channel_id
        text = event.get("text", "")
        thread_ts = event.get("thread_ts") or event["ts"]
        user_id = context.user_id

        # Strip the bot mention from the text
        cleaned_text = re.sub(r"<@[A-Z0-9]+>", "", text).strip()

        if not cleaned_text:
            say(
                text="Hey there! How can I help you? Describe your IT issue and I'll do my best to assist.",
                thread_ts=thread_ts,
            )
            return

        # Add eyes reaction only to the first message (not threaded replies)
        if not event.get("thread_ts"):
            client.reactions_add(
                channel=channel_id,
                timestamp=event["ts"],
                name="eyes",
            )
        ...
```

</TabItem>
<TabItem value="message" label = "Message">

```python
from logging import Logger

from slack_bolt.context import BoltContext
from slack_bolt.context.say import Say
from slack_bolt.context.say_stream import SayStream
from slack_bolt.context.set_status import SetStatus
from slack_sdk import WebClient

from agent import CaseyDeps, run_casey_agent
from thread_context import session_store
from listeners.views.feedback_builder import build_feedback_blocks


def handle_message(
    client: WebClient,
    context: BoltContext,
    event: dict,
    logger: Logger,
    say: Say,
    say_stream: SayStream,
    set_status: SetStatus,
):
    """Handle messages sent to Casey via DM or in threads the bot is part of."""
    # Issue submissions are posted by the bot with metadata so the message
    # handler can run the agent on behalf of the original user.
    is_issue_submission = (
        event.get("metadata", {}).get("event_type") == "issue_submission"
    )

    # Skip message subtypes (edits, deletes, etc.) and bot messages that
    # are not issue submissions.
    if event.get("subtype"):
        return
    if event.get("bot_id") and not is_issue_submission:
        return

    is_dm = event.get("channel_type") == "im"
    is_thread_reply = event.get("thread_ts") is not None

    if is_dm:
        pass
    elif is_thread_reply:
        # Channel thread replies are handled only if the bot is already engaged
        session = session_store.get_session(context.channel_id, event["thread_ts"])
        if session is None:
            return
    else:
        # Top-level channel messages are handled by app_mentioned
        return

    try:
        channel_id = context.channel_id
        text = event.get("text", "")
        thread_ts = event.get("thread_ts") or event["ts"]

        # Get session ID for conversation context
        existing_session_id = session_store.get_session(channel_id, thread_ts)

        # Add eyes reaction only to the first message (DMs only — channel
        # threads already have the reaction from the initial app_mention)
        if is_dm and not existing_session_id:
            await client.reactions_add(
                channel=channel_id,
                timestamp=event["ts"],
                name="eyes",
            )

        ...
```

</TabItem>

<TabItem value="assistant" label = "Assistant thread">

:::tip[Using the Assistant side panel]
The Assistant side panel requires additional setup. See the [Assistant class guide](/tools/bolt-python/concepts/assistant-class).
:::


```py
from logging import Logger

from slack_bolt.context.set_suggested_prompts import SetSuggestedPrompts

SUGGESTED_PROMPTS = [
    {"title": "Reset Password", "message": "I need to reset my password"},
    {"title": "Request Access", "message": "I need access to a system or tool"},
    {"title": "Network Issues", "message": "I'm having network connectivity issues"},
]


def handle_assistant_thread_started(
    set_suggested_prompts: SetSuggestedPrompts, logger: Logger
):
    """Handle assistant thread started events by setting suggested prompts."""
    try:
        set_suggested_prompts(
            prompts=SUGGESTED_PROMPTS,
            title="How can I help you today?",
        )
    except Exception as e:
        logger.exception(f"Failed to handle assistant thread started: {e}")
```

</TabItem>
</Tabs>

---

## Setting status {#setting-assistant-status}

Your app can show actions are happening behind the scenes by setting its thread status. 

```python
def handle_app_mentioned(
    set_status: SetStatus,
    ...
):
    set_status(
        status="Thinking...",
        loading_messages=[
            "Teaching the hamsters to type faster…",
            "Untangling the internet cables…",
            "Consulting the office goldfish…",
            "Polishing up the response just for you…",
            "Convincing the AI to stop overthinking…",
        ],
    )
```

---

## Streaming messages {#text-streaming}

You can have your app's messages stream in to replicate conventional agent behavior. Bolt for Python provides a `say_stream` utility as a listener argument available for `app.event` and `app.message` listeners. 

The `say_stream` utility streamlines calling the Python Slack SDK's [`WebClient.chat_stream`](https://docs.slack.dev/tools/python-slack-sdk/reference/web/client.html#slack_sdk.web.client.WebClient.chat_stream) helper utility by sourcing parameter values from the relevant event payload.

| Parameter | Value |
|---|---| 
| `channel_id` | Sourced from the event payload.
| `thread_ts` | Sourced from the event payload. Falls back to the `ts` value if available.
| `recipient_team_id` | Sourced from the event `team_id` (`enterprise_id` if the app is installed on an org).
| `recipient_user_id` | Sourced from the `user_id` of the event.

If neither a `channel_id` or `thread_ts` can be sourced, then the utility will be `None`.

```python
streamer = say_stream()
streamer.append(markdown_text="Here's my response...")
streamer.append(markdown_text="And here's more...")
streamer.stop()
```

---

## Adding and handling feedback {#adding-and-handling-feedback}

You can use the [feedback buttons block element](/reference/block-kit/block-elements/feedback-buttons-element/) to allow users to immediately provide feedback regarding the app's responses. Here's what the feedback buttons look like from the Support Agent sample app:

```py title=".../listeners/views/feedback_builder.py"
from slack_sdk.models.blocks import (
    Block,
    ContextActionsBlock,
    FeedbackButtonObject,
    FeedbackButtonsElement,
)


def build_feedback_blocks() -> list[Block]:
    """Build feedback blocks with thumbs up/down buttons."""
    return [
        ContextActionsBlock(
            elements=[
                FeedbackButtonsElement(
                    action_id="feedback",
                    positive_button=FeedbackButtonObject(
                        text="Good Response",
                        accessibility_label="Submit positive feedback on this response",
                        value="good-feedback",
                    ),
                    negative_button=FeedbackButtonObject(
                        text="Bad Response",
                        accessibility_label="Submit negative feedback on this response",
                        value="bad-feedback",
                    ),
                )
            ]
        )
    ]
```

That feedback block is then rendered at the bottom of your app's message via the `say_stream` utility.

```py
...
        # Stream response in thread with feedback buttons
        streamer = say_stream()
        streamer.append(markdown_text=result.output)
        feedback_blocks = build_feedback_blocks()
        streamer.stop(blocks=feedback_blocks)
...
```

You can also add a response for when the user provides feedback. 

```python title="...listeners/actions/feedback_button.py"
from logging import Logger

from slack_bolt import Ack, BoltContext
from slack_sdk import WebClient


def handle_feedback_button(
    ack: Ack, body: dict, client: WebClient, context: BoltContext, logger: Logger
):
    """Handle thumbs up/down feedback on Casey's responses."""
    ack()

    try:
        channel_id = context.channel_id
        user_id = context.user_id
        message_ts = body["message"]["ts"]
        feedback_value = body["actions"][0]["value"]

        if feedback_value == "good-feedback":
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                thread_ts=message_ts,
                text="Glad that was helpful! :tada:",
            )
        else:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                thread_ts=message_ts,
                text="Sorry that wasn't helpful. :slightly_frowning_face: Try rephrasing your question or I can create a support ticket for you.",
            )

        logger.debug(
            f"Feedback received: value={feedback_value}, message_ts={message_ts}"
        )
    except Exception as e:
        logger.exception(f"Failed to handle feedback: {e}")
```

---

## Full example

Putting all those concepts together results in a dynamic agent ready to helpfully respond.


<details>
<summary>Full example</summary>
<Tabs>
<TabItem value="pydantic" label = "Pydantic">

```python title="app_mentioned.py"
import re
from logging import Logger

from slack_bolt import BoltContext, Say, SayStream, SetStatus
from slack_sdk import WebClient

from agent import CaseyDeps, casey_agent, get_model
from thread_context import conversation_store
from listeners.views.feedback_builder import build_feedback_blocks


def handle_app_mentioned(
    client: WebClient,
    context: BoltContext,
    event: dict,
    logger: Logger,
    say: Say,
    say_stream: SayStream,
    set_status: SetStatus,
):
    """Handle @Casey mentions in channels."""
    try:
        channel_id = context.channel_id
        text = event.get("text", "")
        thread_ts = event.get("thread_ts") or event["ts"]
        user_id = context.user_id

        # Strip the bot mention from the text
        cleaned_text = re.sub(r"<@[A-Z0-9]+>", "", text).strip()

        if not cleaned_text:
            say(
                text="Hey there! How can I help you? Describe your IT issue and I'll do my best to assist.",
                thread_ts=thread_ts,
            )
            return

        # Add eyes reaction only to the first message (not threaded replies)
        if not event.get("thread_ts"):
            client.reactions_add(
                channel=channel_id,
                timestamp=event["ts"],
                name="eyes",
            )

        # Set assistant thread status with loading messages
        set_status(
            status="Thinking...",
            loading_messages=[
                "Teaching the hamsters to type faster…",
                "Untangling the internet cables…",
                "Consulting the office goldfish…",
                "Polishing up the response just for you…",
                "Convincing the AI to stop overthinking…",
            ],
        )

        # Get conversation history
        history = conversation_store.get_history(channel_id, thread_ts)

        # Run the agent
        deps = CaseyDeps(
            client=client,
            user_id=user_id,
            channel_id=channel_id,
            thread_ts=thread_ts,
            message_ts=event["ts"],
        )
        result = casey_agent.run_sync(
            cleaned_text,
            model=get_model(),
            deps=deps,
            message_history=history,
        )

        # Stream response in thread with feedback buttons
        streamer = say_stream()
        streamer.append(markdown_text=result.output)
        feedback_blocks = build_feedback_blocks()
        streamer.stop(blocks=feedback_blocks)

        # Store conversation history
        conversation_store.set_history(channel_id, thread_ts, result.all_messages())

    except Exception as e:
        logger.exception(f"Failed to handle app mention: {e}")
        say(
            text=f":warning: Something went wrong! ({e})",
            thread_ts=event.get("thread_ts") or event["ts"],
        )
```

</TabItem>
<TabItem value="anthropic" label = "Anthropic">

```python title="app_mentioned.py"
import re
from logging import Logger

from slack_bolt.context import BoltContext
from slack_bolt.context.say import Say
from slack_bolt.context.say_stream import SayStream
from slack_bolt.context.set_status import SetStatus
from slack_sdk import WebClient

from agent import CaseyDeps, run_casey_agent
from thread_context import session_store
from listeners.views.feedback_builder import build_feedback_blocks


def handle_app_mentioned(
    client: WebClient,
    context: BoltContext,
    event: dict,
    logger: Logger,
    say: Say,
    say_stream: SayStream,
    set_status: SetStatus,
):
    """Handle @Casey mentions in channels."""
    try:
        channel_id = context.channel_id
        text = event.get("text", "")
        thread_ts = event.get("thread_ts") or event["ts"]

        # Strip the bot mention from the text
        cleaned_text = re.sub(r"<@[A-Z0-9]+>", "", text).strip()

        if not cleaned_text:
            say(
                text="Hey there! How can I help you? Describe your IT issue and I'll do my best to assist.",
                thread_ts=thread_ts,
            )
            return

        # Add eyes reaction only to the first message (not threaded replies)
        if not event.get("thread_ts"):
            client.reactions_add(
                channel=channel_id,
                timestamp=event["ts"],
                name="eyes",
            )

        # Set assistant thread status with loading messages
        set_status(
            status="Thinking...",
            loading_messages=[
                "Teaching the hamsters to type faster…",
                "Untangling the internet cables…",
                "Consulting the office goldfish…",
                "Polishing up the response just for you…",
                "Convincing the AI to stop overthinking…",
            ],
        )

        # Get session ID for conversation context
        existing_session_id = session_store.get_session(channel_id, thread_ts)

        # Run the agent with deps for tool access
        deps = CaseyDeps(
            client=client,
            user_id=context.user_id,
            channel_id=channel_id,
            thread_ts=thread_ts,
            message_ts=event["ts"],
        )
        response_text, new_session_id = run_casey_agent(
            cleaned_text, session_id=existing_session_id, deps=deps
        )

        # Stream response in thread with feedback buttons
        streamer = say_stream()
        streamer.append(markdown_text=response_text)
        feedback_blocks = build_feedback_blocks()
        streamer.stop(blocks=feedback_blocks)

        # Store session ID for future context
        if new_session_id:
            session_store.set_session(channel_id, thread_ts, new_session_id)

    except Exception as e:
        logger.exception(f"Failed to handle app mention: {e}")
        await say(
            text=f":warning: Something went wrong! ({e})",
            thread_ts=event.get("thread_ts") or event["ts"],
        )
```
</TabItem>
<TabItem value="openai" label = "OpenAI">

```python title="app_mentioned.py"
import re
from logging import Logger

from agents import Runner
from slack_bolt import BoltContext, Say, SayStream, SetStatus
from slack_sdk import WebClient

from agent import CaseyDeps, casey_agent
from thread_context import conversation_store
from listeners.views.feedback_builder import build_feedback_blocks


def handle_app_mentioned(
    client: WebClient,
    context: BoltContext,
    event: dict,
    logger: Logger,
    say: Say,
    say_stream: SayStream,
    set_status: SetStatus,
):
    """Handle @Casey mentions in channels."""
    try:
        channel_id = context.channel_id
        text = event.get("text", "")
        thread_ts = event.get("thread_ts") or event["ts"]
        user_id = context.user_id

        # Strip the bot mention from the text
        cleaned_text = re.sub(r"<@[A-Z0-9]+>", "", text).strip()

        if not cleaned_text:
            say(
                text="Hey there! How can I help you? Describe your IT issue and I'll do my best to assist.",
                thread_ts=thread_ts,
            )
            return

        # Add eyes reaction only to the first message (not threaded replies)
        if not event.get("thread_ts"):
            client.reactions_add(
                channel=channel_id,
                timestamp=event["ts"],
                name="eyes",
            )

        # Set assistant thread status with loading messages
        set_status(
            status="Thinking...",
            loading_messages=[
                "Teaching the hamsters to type faster…",
                "Untangling the internet cables…",
                "Consulting the office goldfish…",
                "Polishing up the response just for you…",
                "Convincing the AI to stop overthinking…",
            ],
        )

        # Get conversation history
        history = conversation_store.get_history(channel_id, thread_ts)

        # Build input for the agent
        if history:
            input_items = history + [{"role": "user", "content": cleaned_text}]
        else:
            input_items = cleaned_text

        # Run the agent
        deps = CaseyDeps(
            client=client,
            user_id=user_id,
            channel_id=channel_id,
            thread_ts=thread_ts,
            message_ts=event["ts"],
        )
        result = Runner.run_sync(casey_agent, input=input_items, context=deps)

        # Stream response in thread with feedback buttons
        streamer = say_stream()
        streamer.append(markdown_text=result.final_output)
        feedback_blocks = build_feedback_blocks()
        streamer.stop(blocks=feedback_blocks)

        # Store conversation history
        conversation_store.set_history(channel_id, thread_ts, result.to_input_list())

    except Exception as e:
        logger.exception(f"Failed to handle app mention: {e}")
        say(
            text=f":warning: Something went wrong! ({e})",
            thread_ts=event.get("thread_ts") or event["ts"],
        )
```

</TabItem>
</Tabs>
</details>

---

## Onward: adding custom tools

Casey comes with test tools and simulated systems. You can extend it with custom tools to make it a fully functioning Slack agent.

In this example, we'll add a tool that makes live calls to check the GitHub status.

1. Create `agent/tools/{tool-name}.py` and define the tool with the `@tool` decorator:

```python title="agent/tools/check_github_status.py"
from claude_agent_sdk import tool
import httpx

@tool(
    name="check_github_status",
    description="Check GitHub's current operational status",
    input_schema={},
)
async def check_github_status_tool(args):
    """Check if GitHub is operational."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.githubstatus.com/api/v2/status.json")
        data = response.json()
        status = data["status"]["indicator"]
        description = data["status"]["description"]
    
    return {
        "content": [
            {
                "type": "text",
                "text": f"**GitHub Status** — {status}\n{description}",
            }
        ]
    }
```

2. Import the tool in `agent/casey.py`:

```python title="agent/casey.py"
from agent.tools import check_github_status_tool
```

3. Register in `casey_tools_server`:

```python title="agent/casey.py"
casey_tools_server = create_sdk_mcp_server(
    name="casey-tools",
    version="1.0.0",
    tools=[
        check_github_status_tool,  # Add here
        # ... other tools
    ],
)
```

4. Add to `CASEY_TOOLS`:

```python title="agent/casey.py"
CASEY_TOOLS = [
    "check_github_status",  # Add here
    # ... other tools
]
```

Use this example as a jumping off point for building out an agent with the capabilities you need!