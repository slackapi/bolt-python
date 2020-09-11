---
title: Listening for view submissions
lang: en
slug: view_submissions
order: 12
---

<div class="section-content">

If a <a href="https://api.slack.com/reference/block-kit/views">view payload</a> contains any input blocks, you must listen to `view_submission` events to receive their values. To listen to `view_submission` events, you can use the built-in `view()` method. `view()` requires a `callback_id` of type `str` or `RegExp`.

You can access the value of the `input` blocks by accessing the `state` object. `state` contains a `values` object that uses the `block_id` and unique `action_id` to store the input values.

Read more about view submissions in our <a href="https://api.slack.com/surfaces/modals/using#interactions">API documentation</a>.

</div>

```python
# Handle a view_submission event
@app.view("view_b")
def handle_submission(ack, body, client, view):
    # Acknowledge the view_submission event
    ack()

    # Do whatever you want with the input data - here we're saving it to a DB then sending the user a verifcation of their submission

    # Assume there's an input block with `block_1` as the block_id and `input_a`
    val = view["state"]["values"]["block_1"]["input_a"]
    user = body["user"]["id"]

    # Message to send user
    msg = ""

    # TODO: Store in DB

    if results:
      msg = "Your submission was successful"
    else:
      msg = "There was an error with your submission"

    # Message the user
    client.chat_postMessage(channel=user, text=msg)
```
