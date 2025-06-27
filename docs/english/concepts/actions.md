---
title: Listening & responding to actions
lang: en
slug: /concepts/actions
---

Your app can listen and respond to user actions, like button clicks, and menu selects, using the `action` method.

## Listening to actions

Actions can be filtered on an `action_id` parameter of type `str` or `re.Pattern`. The `action_id` parameter acts as a unique identifier for interactive components on the Slack platform.

You'll notice in all `action()` examples, `ack()` is used. It is required to call the `ack()` function within an action listener to acknowledge that the request was received from Slack. This is discussed in the [acknowledging requests guide](/concepts/acknowledge).

Refer to [the module document](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.

```python
# Your listener will be called every time a block element with the action_id "approve_button" is triggered
@app.action("approve_button")
def update_message(ack):
    ack()
    # Update the message to reflect the action
```

### Listening to actions using a constraint object

You can use a constraints object to listen to `block_id`s and `action_id`s (or any combination of them). Constraints in the object can be of type `str` or `re.Pattern`.

```python
# Your function will only be called when the action_id matches 'select_user' AND the block_id matches 'assign_ticket'
@app.action({
    "block_id": "assign_ticket",
    "action_id": "select_user"
})
def update_message(ack, body, client):
    ack()

    if "container" in body and "message_ts" in body["container"]:
        client.reactions_add(
            name="white_check_mark",
            channel=body["channel"]["id"],
            timestamp=body["container"]["message_ts"],
        )
```

## Responding to actions

There are two main ways to respond to actions. The first (and most common) way is to use `say()`, which sends a message back to the conversation where the incoming request took place.

The second way to respond to actions is using `respond()`, which is a utility to use the `response_url` associated with the action.

Refer to [the module document](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.

```python
# Your listener will be called every time an interactive component with the action_id “approve_button” is triggered
@app.action("approve_button")
def approve_request(ack, say):
    # Acknowledge action request
    ack()
    say("Request approved 👍")
```

### Using `respond()` method

Since `respond()` is a utility for calling the `response_url`, it behaves in the same way. You can pass [all the message payload properties](https://docs.slack.dev/messaging/#payloads) as keyword arguments along with optional properties like `response_type` (which has a value of `"in_channel"` or `"ephemeral"`), `replace_original`, `delete_original`, `unfurl_links`, and `unfurl_media`. With that, your app can send a new message payload that will be published back to the source of the original interaction.

```python
# Listens to actions triggered with action_id of “user_select”
@app.action("user_select")
def select_user(ack, action, respond):
    ack()
    respond(f"You selected <@{action['selected_user']}>")
```