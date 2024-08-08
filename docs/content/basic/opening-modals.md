---
title: Opening modals
lang: en
slug: /concepts/opening-modals
---

[Modals](https://api.slack.com/block-kit/surfaces/modal)s are focused surfaces that allow you to collect user data and display dynamic information. You can open a modal by passing a valid `trigger_id` and a [view payload](https://api.slack.com/reference/block-kit/views) to the built-in client's [`views.open`](https://api.slack.com/methods/views.open) method.

Your app receives `trigger_id`s in payloads sent to your Request URL that are triggered by user invocations, like a shortcut, button press, or interaction with a select menu.

Read more about modal composition in the [API documentation](https://api.slack.com/surfaces/modals/using#composing_views).

Refer to [the module document](https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.

```python
# Listen for a shortcut invocation
@app.shortcut("open_modal")
def open_modal(ack, body, client):
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "My App"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Welcome to a modal with _blocks_"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Click me!"},
                        "action_id": "button_abc"
                    }
                },
                {
                    "type": "input",
                    "block_id": "input_c",
                    "label": {"type": "plain_text", "text": "What are your hopes and dreams?"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "dreamy_input",
                        "multiline": True
                    }
                }
            ]
        }
    )
```