---
title: Listening & responding to commands
lang: en
slug: /concepts/commands
---

Your app can use the `command()` method to listen to incoming slash command requests. The method requires a `command_name` of type `str`.

Commands must be acknowledged with `ack()` to inform Slack your app has received the request.

There are two ways to respond to slash commands. The first way is to use `say()`, which accepts a string or JSON payload. The second is `respond()` which is a utility for the `response_url`. These are explained in more depth in the [responding to actions](/bolt-python/concepts/actions) section.

When setting up commands within your app configuration, you'll append `/slack/events` to your request URL.

Refer to [the module document](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.
```python
# The echo command simply echoes on command
@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")
```
