---
title: Listening to messages
lang: en
slug: /concepts/message-listening
---

To listen to messages that [your app has access to receive](https://docs.slack.dev/messaging/retrieving-messages), you can use the `message()` method which filters out events that aren't of type `message`.

`message()` accepts an argument of type `str` or `re.Pattern` object that filters out any messages that don't match the pattern.

:::info

Refer to [the module document](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.

:::

```python
# This will match any message that contains 👋
@app.message(":wave:")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")
```

## Using a regular expression pattern

The `re.compile()` method can be used instead of a string for more granular matching.

```python
import re

@app.message(re.compile("(hi|hello|hey)"))
def say_hello_regex(say, context):
    # regular expression matches are inside of context.matches
    greeting = context['matches'][0]
    say(f"{greeting}, how are you?")
```