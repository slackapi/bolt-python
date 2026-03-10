# Experiments

Bolt for Python includes experimental features still under active development. These features may be fleeting, may not be perfectly polished, and should be thought of as available for use "at your own risk."

Experimental features are categorized as `semver:patch` until the experimental status is removed.

We love feedback from our community, so we encourage you to explore and interact with the [GitHub repo](https://github.com/slackapi/bolt-python). Contributions, bug reports, and any feedback are all helpful; let us nurture the Slack CLI together to help make building Slack apps more pleasant for everyone.

## Available experiments
* [say_stream listener argument](#say-stream)

## say_stream listener argument {#say-stream}

The `say_stream: SayStream` listener argument provides access to streaming chat for AI agents.

`SayStream` and `AsyncSayStream` are callable context utilities pre-configured with event context defaults: `channel_id`, `thread_ts`, `team_id`, and `user_id`.

### Example

```python
from slack_bolt import SayStream

@app.event("app_mention")
def handle_mention(say_stream: SayStream):
    stream = say_stream()
    stream.append(markdown_text="Hello!")
    stream.stop()
```

### Limitations

`say_stream()` requires either `thread_ts` or `event.ts` in the event context. It works in DMs, threaded replies, and top-level messages with a `ts` field.
