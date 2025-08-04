---
title: Listener middleware
lang: en
slug: /bolt-python/concepts/listener-middleware
---

Listener middleware is only run for the listener in which it's passed. You can pass any number of middleware functions to the listener using the `middleware` parameter, which must be a list that contains one to many middleware functions.

If your listener middleware is a quite simple one, you can use a listener matcher, which returns `bool` value (`True` for proceeding) instead of requiring `next()` method call.

Refer to [the module document](https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.

```python
# Listener middleware which filters out messages from a bot
def no_bot_messages(message, next):
    if "bot_id" not in message:
        next()

# This listener only receives messages from humans
@app.event(event="message", middleware=[no_bot_messages])
def log_message(logger, event):
    logger.info(f"(MSG) User: {event['user']}\nMessage: {event['text']}")

# Listener matchers: simplified version of listener middleware
def no_bot_messages(message) -> bool:
    return "bot_id" not in message

@app.event(
    event="message",
    matchers=[no_bot_messages]
    # or matchers=[lambda message: message.get("subtype") != "bot_message"]
)
def log_message(logger, event):
    logger.info(f"(MSG) User: {event['user']}\nMessage: {event['text']}")
```
