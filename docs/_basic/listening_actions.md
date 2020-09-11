---
title: Listening to actions
lang: en
slug: action-listening
order: 5
---

<div class="section-content">
Your app can listen to user actions like button clicks, and menu selects, using the `action` method.

Actions can be filtered on an `action_id` of type `str` or `RegExp` object. `action_id`s act as unique identifiers for interactive components on the Slack platform.

You’ll notice in all `action()` examples, `ack()` is used. It is required to call the `ack()` function within an action listener to acknowledge that the event was received from Slack. This is discussed in the [acknowledging events section](#acknowledge).

</div>

```python
# Your middleware will be called every time an interactive component with the action_id "approve_button" is triggered
@app.action("approve_button")
def update_message(ack):
    ack()
    # Update the message to reflect the action
```

<details class="secondary-wrapper">
<summary class="section-head" markdown="0">
<h4 class="section-head">Listening to actions using a constraint object</h4>
</summary>

<div class="secondary-content" markdown="0">

You can use a constraints object to listen to `callback_id`s, `block_id`s, and `action_id`s (or any combination of them). Constraints in the object can be of type `str` or `RegExp` object.

</div>

```python
# Your function will only be called when the action_id matches 'select_user' AND the block_id matches 'assign_ticket'
@app.action({"action_id": "select_user", "block_id": "assign_ticket"})
def update_message(ack, action, client):
    ack()
    client.reactions_add(name='white_check_mark',
                         timestamp=action['ts'],
                         channel=action['channel'])
```

</details>
