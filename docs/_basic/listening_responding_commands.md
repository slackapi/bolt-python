---
title: Listening and responding to commands
lang: en
slug: commands
order: 9
---

<div class="section-content">

Your app can use the `command()` method to listen to incoming slash command events. The method requires a `command_name` of type `str`.

Commands must be acknowledged with `ack()` to inform Slack your app has received the event.

There are two ways to respond to slash commands. The first way is to use `say()`, which accepts a string or JSON payload. The second is `respond()` which is a utility for the `response_url`. These are explained in more depth in the [responding to actions](#action-respond) section.

When configuring commands within your app configuration, you'll continue to append `/slack/events` to your request URL.

</div>

```python
# The echo command simply echoes on command
@app.command("/echo")
def repeat_text(ack, say, command):
    # Acknowledge command request
    ack()
    say(f"{command['text']}")
```
