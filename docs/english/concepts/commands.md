# Listening & responding to commands

Your app can use the `command()` method to listen to incoming slash command requests. The method requires a `command_name` of type `str`.

Commands must be acknowledged with `ack()` to inform Slack your app has received the request.

There are two ways to respond to slash commands. The first way is to use `say()`, which accepts a string or JSON payload. The second is `respond()` which is a utility for the `response_url`. These are explained in more depth in the [responding to actions](/tools/bolt-python/concepts/actions) section.

When setting up commands within your app configuration, you'll append `/slack/events` to your request URL.

Refer to [the module document](https://docs.slack.dev/tools/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.

## Example

```python
# The echo command simply echoes on command
@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")
```
