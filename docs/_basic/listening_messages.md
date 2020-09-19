---
title: Listening to messages
lang: en
slug: message-listening
order: 1
---

<div class="section-content">

To listen to messages that [your app has access to receive](https://api.slack.com/messaging/retrieving#permissions), you can use the `message()` method which filters out events that aren’t of type `message`.

`message()` accepts an argument of type `str` or `RegEx` object that filters out any messages that don’t match the pattern.

</div>

```python
# This will match any message that contains 👋
@app.message(":wave:")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")
```

<details class="secondary-wrapper">
<summary markdown="0">
<h4 class="secondary-header">Using a RegEx pattern</h4>
</summary>

<div class="secondary-content" markdown="0">

The `re.compile()` method can be used instead of a string for more granular matching.

</div>

```python
@app.message(re.compile("(hi|hello|hey)"))
def say_hello_regex(say, context):
    # RegEx matches are inside of context.matches
    greeting = context['matches'][0]
    say(f"{greeting}, how are you?")
```

</details>
