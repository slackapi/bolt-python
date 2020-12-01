---
title: Listening for view submissions
lang: en
slug: view_submissions
order: 12
---

<div class="section-content">

If a <a href="https://api.slack.com/reference/block-kit/views">view payload</a> contains any input blocks, you must listen to `view_submission` events to receive their values. To listen to `view_submission` events, you can use the built-in `view()` method. `view()` requires a `callback_id` of type `str` or `re.Pattern`.

You can access the value of the `input` blocks by accessing the `state` object. `state` contains a `values` object that uses the `block_id` and unique `action_id` to store the input values.

Read more about view submissions in our <a href="https://api.slack.com/surfaces/modals/using#interactions">API documentation</a>.

</div>

```python
# Handle a view_submission event
@app.view("view_1")
def handle_submission(ack, body, client, view):
    # Assume there's an input block with `block_c` as the block_id and `dreamy_input`
    hopes_and_dreams = view["state"]["values"]["block_c"]["dreamy_input"]
    user = body["user"]["id"]
    # Validate the inputs
    errors = {}
    if hopes_and_dreams is not None and len(hopes_and_dreams) <= 5:
        errors["block_c"] = "The value must be longer than 5 characters"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return
    # Acknowledge the view_submission event and close the modal
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission

    # Message to send user
    msg = ""
    try:
        # Save to DB
        msg = f"Your submission of {hopes_and_dreams} was successful"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"
    finally:
        # Message the user
        client.chat_postMessage(channel=user, text=msg)
```
