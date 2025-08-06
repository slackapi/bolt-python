# Listening & responding to shortcuts

The `shortcut()` method supports both [global shortcuts](/interactivity/implementing-shortcuts#global) and [message shortcuts](/interactivity/implementing-shortcuts#messages).

Shortcuts are invokable entry points to apps. Global shortcuts are available from within search and text composer area in Slack. Message shortcuts are available in the context menus of messages. Your app can use the `shortcut()` method to listen to incoming shortcut requests. The method requires a `callback_id` parameter of type `str` or `re.Pattern`.

Shortcuts must be acknowledged with `ack()` to inform Slack that your app has received the request.

Shortcuts include a `trigger_id` which an app can use to [open a modal](/tools/bolt-python/concepts/opening-modals) that confirms the action the user is taking.

When setting up shortcuts within your app configuration, as with other URLs, you'll append `/slack/events` to your request URL.

⚠️ Note that global shortcuts do **not** include a channel ID. If your app needs access to a channel ID, you may use a [`conversations_select`](/reference/block-kit/block-elements/multi-select-menu-element#conversation_multi_select) element within a modal. Message shortcuts do include a channel ID.

Refer to [the module document](https://docs.slack.dev/tools/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.
```python
# The open_modal shortcut listens to a shortcut with the callback_id "open_modal"
@app.shortcut("open_modal")
def open_modal(ack, shortcut, client):
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        # A simple view payload for a modal
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "My App"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "About the simplest modal you could conceive of :smile:\n\nMaybe </block-kit/#making-things-interactive|*make the modal interactive*> or </surfaces/modals|*learn more advanced modal use cases*>."
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>"
                        }
                    ]
                }
            ]
        }
    )
```

## Listening to shortcuts using a constraint object

You can use a constraints object to listen to `callback_id`s, and `type`s. Constraints in the object can be of type `str` or `re.Pattern`.
  
```python
# Your listener will only be called when the callback_id matches 'open_modal' AND the type matches 'message_action'
@app.shortcut({"callback_id": "open_modal", "type": "message_action"})
def open_modal(ack, shortcut, client):
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using one of the built-in WebClients
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "My App"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "About the simplest modal you could conceive of :smile:\n\nMaybe </block-kit/#making-things-interactive|*make the modal interactive*> or </surfaces/modals|*learn more advanced modal use cases*>."
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>"
                        }
                    ]
                }
            ]
        }
    )
```