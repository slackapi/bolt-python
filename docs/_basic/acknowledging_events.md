---
title: Acknowledging events
lang: en
slug: acknowledge
order: 7
---

<div class="section-content">

Actions, commands, and options events must **always** be acknowledged using the `ack()` function. This lets Slack know that the event was received and updates the Slack user interface accordingly.

Depending on the type of event, your acknowledgement may be different. For example, when acknowledging a dialog submission you will call `ack()` with validation errors if the submission contains errors, or with no parameters if the submission is valid.

We recommend calling `ack()` right away before sending a new message or fetching information from your database since you only have 3 seconds to respond.

</div>

```python
# Listen for dialog submissions with a callback_id of ticket_submit
@app.action("ticket_submit")
def process_submission(ack, action):
    # Regex to determine if this is a valid email
    is_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    if re.match(is_email, action["submission"]["email"]):
        # It’s a valid email, accept the submission
        ack()
    else:
        # If it isn’t a valid email, acknowledge with an error
        errors = [{
            "name": "email_address",
            "error": "Sorry, this isn’t a valid email"
        }]
        ack({"errors": errors})
```
