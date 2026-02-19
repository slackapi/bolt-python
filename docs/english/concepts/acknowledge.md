# Acknowledging requests

Actions, commands, shortcuts, options requests, and view submissions must **always** be acknowledged using the `ack()` function. This lets Slack know that the request was received so that it may update the Slack user interface accordingly.

Depending on the type of request, your acknowledgement may be different. For example, when acknowledging a menu selection associated with an external data source, you would call `ack()` with a list of relevant [options](/reference/block-kit/composition-objects/option-object/). When acknowledging a view submission, you may supply a `response_action` as part of your acknowledgement to [update the view](/tools/bolt-python/concepts/view-submissions). 

We recommend calling `ack()` right away before initiating any time-consuming processes such as fetching information from your database or sending a new message, since you only have 3 seconds to respond before Slack registers a timeout error.

:::info[When working in a FaaS / serverless environment, our guidelines for when to `ack()` are different. See the section on [Lazy listeners (FaaS)](/tools/bolt-python/concepts/lazy-listeners) for more detail on this.]

:::

Refer to [the module document](https://docs.slack.dev/tools/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.

## Example

```python
# Example of responding to an external_select options request
@app.options("menu_selection")
def show_menu_options(ack):
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
