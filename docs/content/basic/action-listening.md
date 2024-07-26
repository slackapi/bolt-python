---
title: Listening to actions
lang: en
slug: /concepts/action-listening
---

Your app can listen to user actions, like button clicks, and menu selects, using the `action` method.

Actions can be filtered on an `action_id` of type `str` or `re.Pattern`. `action_id`s act as unique identifiers for interactive components on the Slack platform.

You'll notice in all `action()` examples, `ack()` is used. It is required to call the `ack()` function within an action listener to acknowledge that the request was received from Slack. This is discussed in the [acknowledging requests section](/concepts/acknowledge).

Refer to [the module document](https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.
```python
# Your listener will be called every time a block element with the action_id "approve_button" is triggered
@app.action("approve_button")
def update_message(ack):
    ack()
    # Update the message to reflect the action
```

<details>
<summary>
Listening to actions using a constraint object
</summary>

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

</details>