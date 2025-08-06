# Updating & pushing views

Modals contain a stack of views. When you call [`views_open`](https://api./reference/methods/views.open/slack.com/methods/views.open), you add the root view to the modal. After the initial call, you can dynamically update a view by calling [`views_update`](/reference/methods/views.update/), or stack a new view on top of the root view by calling [`views_push`](/reference/methods/views.push/)

## The `views_update` method

To update a view, you can use the built-in client to call `views_update` with the `view_id` that was generated when you opened the view, and a new `view` including the updated `blocks` list. If you're updating the view when a user interacts with an element inside of an existing view, the `view_id` will be available in the `body` of the request.

## The `views_push` method

To push a new view onto the view stack, you can use the built-in client to call `views_push` with a valid `trigger_id` a new [view payload](/reference/interaction-payloads/view-interactions-payload/#view_submission). The arguments for `views_push` is the same as [opening modals](/tools/bolt-python/concepts/opening-modals). After you open a modal, you may only push two additional views onto the view stack.

Learn more about updating and pushing views in our [API documentation](/surfaces/modals)

Refer to [the module document](https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.
```python
# Listen for a button invocation with action_id `button_abc` (assume it's inside of a modal)
@app.action("button_abc")
def update_modal(ack, body, client):
    # Acknowledge the button request
    ack()
    # Call views_update with the built-in client
    client.views_update(
        # Pass the view_id
        view_id=body["view"]["id"],
        # String that represents view state to protect against race conditions
        hash=body["view"]["hash"],
        # View payload with updated blocks
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "Updated modal"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": "You updated the modal!"}
                },
                {
                    "type": "image",
                    "image_url": "https://media.giphy.com/media/SVZGEcYt7brkFUyU90/giphy.gif",
                    "alt_text": "Yay! The modal was updated"
                }
            ]
        }
    )
```