---
title: Using the Web API
lang: en
slug: web-api
order: 4
---

<div class="section-content">
You can call [any Web API method](https://api.slack.com/methods) using the [`WebClient`](https://slack.dev/node-slack-sdk/web-api) provided to your Bolt app as `app.client` (given that your app has the appropriate scopes). When you call one the client’s methods, it returns a `SlackResponse` which contains the response from Slack.

The token used to initialize Bolt can be found in the `context` object, which is required for most Web API methods.

</div>

```python
@app.message("wake me up")
def say_hello(client, payload):
    # Unix Epoch time for September 30, 2020 11:59:59 PM
    when_september_ends = 1601510399
    channel_id = payload['event']['channel']
    client.chat_scheduleMessage(channel=channel_id,
                                post_at=when_september_ends,
                                text="Summer has come and passed")
```
