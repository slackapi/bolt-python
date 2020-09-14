---
title: Listening to events
lang: en
slug: event-listening
order: 3
---

<div class="section-content">

You can listen to [any Events API event](https://api.slack.com/events) using the `event()` method after subscribing to it in your app configuration. This allows your app to take action when something happens in Slack, like a user reacting to a message or joining a channel.

The `event()` method requires an `eventType` of type `str`.

</div>

```python
# When a user joins the team, send a message in a predefined channel asking them to introduce themselves
@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "C12345";
    user_id = event["user"]["id"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
    say(text=text, channel=welcome_channel_id)
```

<details class="secondary-wrapper" >
  
<summary class="section-head" markdown="0">
  <h4 class="section-head">Filtering on message subtypes</h4>
</summary>

<div class="secondary-content" markdown="0">
The `message()` listener is equivalent to `event("message")`.

You can filter on subtypes of events by passing in the additional key `subtype`. Common message subtypes like `bot_message` and `message_replied` can be found [on the message event page](https://api.slack.com/events/message#message_subtypes).

</div>

```python
# Matches all messages from bot users
@app.message({"subtype": "message_changed"})
def log_message_change(logger, message):
    logger.info(f"The user {message['user']} changed the message to {message['text']}")
```

</details>
