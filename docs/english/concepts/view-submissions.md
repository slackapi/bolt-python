---
title: Listening to views
lang: en
slug: /concepts/view_submissions
---

If a [view payload](https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/#view_submission) contains any input blocks, you must listen to `view_submission` requests to receive their values. To listen to `view_submission` requests, you can use the built-in `view()` method. `view()` requires a `callback_id` of type `str` or `re.Pattern`.

You can access the value of the `input` blocks by accessing the `state` object. `state` contains a `values` object that uses the `block_id` and unique `action_id` to store the input values.

---

##### Update views on submission

To update a view in response to a `view_submission` event, you may pass a `response_action` of type `update` with a newly composed `view` to display in your acknowledgement.

```python
# Update the view on submission 
@app.view("view_1")
def handle_submission(ack, body):
    # The build_new_view() method returns a modal view
    # To build a modal view, we recommend using Block Kit Builder:
    # https://app.slack.com/block-kit-builder/#%7B%22type%22:%22modal%22,%22callback_id%22:%22view_1%22,%22title%22:%7B%22type%22:%22plain_text%22,%22text%22:%22My%20App%22,%22emoji%22:true%7D,%22blocks%22:%5B%5D%7D
    ack(response_action="update", view=build_new_view(body))
```
Similarly, there are options for [displaying errors](https://docs.slack.dev/surfaces/modals#displaying_errors) in response to view submissions.

Read more about view submissions in our [API documentation](https://docs.slack.dev/surfaces/modals#interactions)

---

##### Handling views on close

When listening for `view_closed` requests, you must pass `callback_id` and add a `notify_on_close` property to the view during creation. See below for an example of this:

See the [API documentation](https://docs.slack.dev/surfaces/modals#interactions) for more information about `view_closed`.

```python

client.views_open(
    trigger_id=body.get("trigger_id"),
    view={
        "type": "modal",
        "callback_id": "modal-id",  # Used when calling view_closed
        "title": {
            "type": "plain_text",
            "text": "Modal title"
        },
        "blocks": [],
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "notify_on_close": True,  # This attribute is required
    }
)

# Handle a view_closed request
@app.view_closed("modal-id")
def handle_view_closed(ack, body, logger):
    ack()
    logger.info(body)
```

Refer to [the module document](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.
```python
# Handle a view_submission request
@app.view("view_1")
def handle_submission(ack, body, client, view, logger):
    # Assume there's an input block with `input_c` as the block_id and `dreamy_input`
    hopes_and_dreams = view["state"]["values"]["input_c"]["dreamy_input"]
    user = body["user"]["id"]
    # Validate the inputs
    errors = {}
    if hopes_and_dreams is not None and len(hopes_and_dreams) <= 5:
        errors["input_c"] = "The value must be longer than 5 characters"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return
    # Acknowledge the view_submission request and close the modal
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

    # Message the user
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")
```
