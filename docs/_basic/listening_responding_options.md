---
title: Listening and responding to options
lang: en
slug: options
order: 14
---

<div class="section-content">
The `options()` method listens for incoming option request payloads from Slack. [Similar to `action()`](#action-listening),
an `action_id` or constraints object is required. In order to load external data into your select menus, you must provide an options load URL in your app configuration, appended with `/slack/events`.

While it's recommended to use `action_id` for `external_select` menus, dialogs do not support Block Kit so you'll have to use the constraints object to filter on a `callback_id`.

To respond to options requests, you'll need to call `ack()` with a valid `options` or `option_groups` list. Both [external select response examples](https://api.slack.com/reference/messaging/block-elements#external-select) and [dialog response examples](https://api.slack.com/dialogs#dynamic_select_elements_external) can be found on our API site.

</div>

<div>
<span class="annotation">Refer to <a href="https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html" target="_blank">the module document</a> to learn the available listener arguments.</span>
```python
# Example of responding to an external_select options request
@app.options("external_action")
def show_options(ack):
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
    ack(options=options)
```
</div>