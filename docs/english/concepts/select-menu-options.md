# Listening & responding to select menu options

The `options()` method listens for incoming option request payloads from Slack. [Similar to `action()`](/tools/bolt-python/concepts/actions),
an `action_id` or constraints object is required. In order to load external data into your select menus, you must provide an options load URL in your app configuration, appended with `/slack/events`.

While it's recommended to use `action_id` for `external_select` menus, dialogs do not support Block Kit so you'll have to use the constraints object to filter on a `callback_id`.

To respond to options requests, you'll need to call `ack()` with a valid `options` or `option_groups` list. Both [external select response examples](/reference/block-kit/block-elements/multi-select-menu-element#external_multi_select) and [dialog response examples](/reference/block-kit/block-elements/multi-select-menu-element#conversation_multi_select) can be found on our API site.

Additionally, you may want to apply filtering logic to the returned options based on user input. This can be accomplished by using the `payload` argument to your options listener and checking for the contents of the `value` property within it. Based on the `value` you can return different options. All listeners and middleware handlers in Bolt for Python have access to [many useful arguments](https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html) - be sure to check them out!

Refer to [the module document](https://docs.slack.dev/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.
```python
# Example of responding to an external_select options request
@app.options("external_action")
def show_options(ack, payload):
    options = [
        {
            "text": {"type": "plain_text", "text": "Option 1"},
            "value": "1-1",
        },
        {
            "text": {"type": "plain_text", "text": "Option 2"},
            "value": "1-2",
        },
    ]
    keyword = payload.get("value")
    if keyword is not None and len(keyword) > 0:
        options = [o for o in options if keyword in o["text"]["text"]]
    ack(options=options)
```