---
title: Opening modals
lang: en
slug: /concepts/opening-modals
---

[Modals](https://docs.slack.dev/surfaces/modals) are focused surfaces that allow you to collect user data and display dynamic information. You can open a modal by passing a valid `trigger_id` and a [view payload](https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/#view_submission) to the built-in client's [`views.open`](https://docs.slack.dev/reference/methods/views.open/) method. 

Your app receives `trigger_id` parameters in payloads sent to your Request URL triggered user invocation like a slash command, button press, or interaction with a select menu.

Read more about modal composition in the [API documentation](https://docs.slack.dev/surfaces/modals#composing_views).

Refer to [the module document](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn the available listener arguments.

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
