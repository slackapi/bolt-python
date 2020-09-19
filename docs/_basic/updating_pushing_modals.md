---
title: Updating and pushing views
lang: en
slug: updating-pushing-views
order: 11
---

<div class="section-content">

Modals contain a stack of views. When you call <a href="https://api.slack.com/methods/views.open">`views_open`</a>, you add the root view to the modal. After the initial call, you can dynamically update a view by calling <a href="https://api.slack.com/methods/views.update">`views_update`</a>, or stack a new view on top of the root view by calling <a href="https://api.slack.com/methods/views.push">`views_push`</a>.

<strong><code>views_update</code></strong><br>
To update a view, you can use the built-in client to call <code>views_update</code> with the <code>view_id</code> that was generated when you opened the view, and a new <code>view</code> including the updated <code>blocks</code> array. If you're updating the view when a user interacts with an element inside of an existing view, the <code>view_id</code> will be available in the <code>body</code> of the request.

<strong><code>views_push</code></strong><br>
To push a new view onto the view stack, you can use the built-in client to call <code>views_push</code> with a valid <code>trigger_id</code> a new <a href="https://api.slack.com/reference/block-kit/views">view payload</a>. The arguments for `views_push` is the same as <a href="#creating-modals">opening modals</a>. After you open a modal, you may only push two additional views onto the view stack.

Learn more about updating and pushing views in our <a href="https://api.slack.com/surfaces/modals/using#modifying">API documentation</a>.

</div>

```python
# Listen for a button invocation with action_id `button_abc` (assume it's inside of a modal)
@app.action("button_abc")
def update_modal(ack, view, client):
    # Acknowledge the button request
    ack()
    client.views_update(
        # Pass the view_id
        view_id=view["id"],
        # View payload with updated blocks
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {
                "type": "plain_text",
                "text": "Updated modal"
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "You updated the modal!"
                    }
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
