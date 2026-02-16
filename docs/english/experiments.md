# Experiments

Bolt for Python includes experimental features still under active development. These features may be fleeting, may not be perfectly polished, and should be thought of as available for use "at your own risk." 

Experimental features are categorized as `semver:patch` until the experimental status is removed.

We love feedback from our community, so we encourage you to explore and interact with the [GitHub repo](https://github.com/slackapi/bolt-python). Contributions, bug reports, and any feedback are all helpful; let us nurture the Slack CLI together to help make building Slack apps more pleasant for everyone.

## Available experiments
* [Agent listener argument](#agent)

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