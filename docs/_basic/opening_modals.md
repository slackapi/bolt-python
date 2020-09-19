---
title: Opening modals
lang: en
slug: opening-modals
order: 10
---

<div class="section-content">
<a href="https://api.slack.com/block-kit/surfaces/modals">Modals</a> are focused surfaces that allow you to collect user data and display dynamic information. You can open a modal by passing a valid <code>trigger_id</code> and a <a href="https://api.slack.com/reference/block-kit/views">view payload</a> to the built-in client's <a href="https://api.slack.com/methods/views.open"><code>views.open</code></a> method.

Your app receives <code>trigger_id</code>s in payloads sent to your Request URL triggered user invocation like a slash command, button press, or interaction with a select menu.

Read more about modal composition in the <a href="https://api.slack.com/surfaces/modals/using#composing_views">API documentation</a>.

</div>

```python
# Listen for a slash command invocation
@app.command("/ticket")
def open_modal(ack, payload, client):
    # Acknowledge the command request
    ack();

    # Call views_open with the built-in client
    client.views_open({
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=payload["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {
                "type": "plain_text",
                "text": "Modal title"
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Welcome to a modal with _blocks_"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Click me!"
                        },
                        "action_id": "button_abc"
                    }
                },
                {
                    "type": "input",
                    "block_id": "input_c",
                    "label": {
                        "type": "plain_text",
                        "text": "What are your hopes and dreams?"
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "dreamy_input",
                        "multiline": True
                    }
                }
            ],
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            }
        }
    })
```
