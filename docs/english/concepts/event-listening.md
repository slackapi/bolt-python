---
title: Listening to events
lang: en
slug: /bolt-python/concepts/event-listening
---

You can listen to [any Events API event](/reference/events) using the `event()` method after subscribing to it in your app configuration. This allows your app to take action when something happens in a workspace where it's installed, like a user reacting to a message or joining a channel.

The `event()` method requires an `eventType` of type `str`.

Refer to [the module document](https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.
```python
# When a user joins the workspace, send a message in a predefined channel asking them to introduce themselves
@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "C12345"
    user_id = event["user"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
    say(text=text, channel=welcome_channel_id)
```

## Filtering on message subtypes

The `message()` listener is equivalent to `event("message")`.

You can filter on subtypes of events by passing in the additional key `subtype`. Common message subtypes like `bot_message` and `message_replied` can be found [on the message event page](/reference/events/message#subtypes).
You can explicitly filter for events without a subtype by explicitly setting `None`.

```python
# Matches all modified messages
@app.event({
    "type": "message",
    "subtype": "message_changed"
})
def log_message_change(logger, event):
    user, text = event["user"], event["text"]
    logger.info(f"The user {user} changed the message to {text}")
```