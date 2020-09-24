---
title: Global middleware
lang: en
slug: global-middleware
order: 6
---

<div class="section-content">
Global middleware is run for all incoming events, before any listener middleware. You can add any number of global middleware to your app by passing `CustomMiddleware` instances to `app.use()`. The middleware function is called with the same arguments as listeners, with an additional `next()` function.

Both global and listener middleware must call `next()` to pass control of the execution chain to the next middleware. 
</div>

```python
@app.use
def authWithAcme(logger, payload, next)
    slackUserId = payload["user"]
    helpChannelId = "C12345"

    try:
        # Look up user in external system using their Slack user ID
        user = acme.lookupBySlackId(slackUserId)
        # Add that to context
        context.user = user
    except Exception as e:
        client.chat_postEphemeral(
            channel: payload["channel"],
            user: slackUserId,
            text: f"Sorry <@{slackUserId}, you aren't registered in Acme or there was an error with authentication. Please post in <#${helpChannelId}> for assistance"
        )

    # Pass control to the next middleware
    next()
```
