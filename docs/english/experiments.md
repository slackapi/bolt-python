# Experiments

Bolt for Python includes experimental features still under active development. These features may be fleeting, may not be perfectly polished, and should be thought of as available for use "at your own risk." 

Experimental features are categorized as `semver:patch` until the experimental status is removed.

We love feedback from our community, so we encourage you to explore and interact with the [GitHub repo](https://github.com/slackapi/bolt-python). Contributions, bug reports, and any feedback are all helpful; let us nurture the Slack CLI together to help make building Slack apps more pleasant for everyone.

## Available experiments
* [Agent listener argument](#agent)
* [`say_stream` utility](#say-stream)

## Agent listener argument {#agent}

The `agent: BoltAgent` listener argument provides access to AI agent-related features.

The `BoltAgent` and `AsyncBoltAgent` classes offer a `chat_stream()` method that comes pre-configured with event context defaults: `channel_id`, `thread_ts`, `team_id`, and `user_id` fields. 

The listener argument is wired into the Bolt `kwargs` injection system, so listeners can declare it as a parameter or access it via the `context.agent` property.

### Example

```python
from slack_bolt import BoltAgent

@app.event("app_mention")
def handle_mention(agent: BoltAgent):
    stream = agent.chat_stream()
    stream.append(markdown_text="Hello!")
    stream.stop()
```

### Limitations

The `chat_stream()` method currently only works when the `thread_ts` field is available in the event context (DMs and threaded replies). Top-level channel messages do not have a `thread_ts` field, and the `ts` field is not yet provided to `BoltAgent`.

## `say_stream` utility {#say-stream}

The `say_stream` utility is a listener argument available on `app.event` and `app.message` listeners. 

The `say_stream` utility streamlines calling the Python Slack SDK's [`WebClient.chat_stream`](https://docs.slack.dev/tools/python-slack-sdk/reference/web/client.html#slack_sdk.web.client.WebClient.chat_stream) helper utility by sourcing parameter values from the relevant event payload.

| Parameter | Value |
|---|---| 
| `channel_id` | Sourced from the event payload.
| `thread_ts` | Sourced from the event payload. Falls back to the `ts` value if available.
| `recipient_team_id` | Sourced from the event `team_id` (`enterprise_id` if the app is installed on an org).
| `recipient_user_id` | Sourced from the `user_id` of the event.

If neither a `channel_id` or `thread_ts` can be sourced, then the utility will merely be `None`.

### Example {#example}

```py
import os

from slack_bolt import App, SayStream
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("app_mention")
def handle_app_mention(client: WebClient, say_stream: SayStream):
  stream = say_stream()
  stream.append(markdown_text="Someone rang the bat signal!")
  stream.stop()

@app.message("")
def handle_message(client: WebClient, say_stream: SayStream):
  stream = say_stream()

  stream.append(markdown_text="Let me consult my *vast knowledge database*...)
  stream.stop()

if __name__ == "__main__":
  SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
```