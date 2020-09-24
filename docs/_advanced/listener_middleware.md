---
title: Listener middleware
lang: en
slug: listener-middleware
order: 5
---

<div class="section-content">
Listener middleware is run only for the listener in which it’s passed. You can pass any number of custom listener middleware of type `CustomMiddleware` instances to the listener after the first (required) parameter.
</div>

```python
# Listener middleware which filters out messages with "bot_message" subtype
def noBotMessages(message, next):
    subtype = message.get("subtype", None)
    if (subtype not "bot_message")
       next()

# This listener only receives messages from humans
@app.message(middleware=[noBotMessages]):
def log_message(logger,message):
    logger.info(f"(MSG) User: {message["user"]}\nMessage: {message["text"]}")
```

