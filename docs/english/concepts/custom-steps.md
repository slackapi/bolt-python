---
title: Listening and responding to custom steps
sidebar_label: Custom Steps
lang: en
slug: /concepts/custom-steps
---

Your app can use the `function()` method to listen to incoming [custom step requests](/workflows/workflow-steps). Custom steps are used in Workflow Builder to build workflows. The method requires a step `callback_id` of type `str`. This `callback_id` must also be defined in your [Function](/reference/app-manifest#functions) definition. Custom steps must be finalized using the `complete()` or `fail()` listener arguments to notify Slack that your app has processed the request.

* `complete()` requires **one** argument: `outputs` of type `dict`. It ends your custom step **successfully** and provides a dictionary containing the outputs of your custom step as per its definition.
* `fail()` requires **one** argument: `error` of type `str`. It ends your custom step **unsuccessfully** and provides a message containing information regarding why your custom step failed.

You can reference your custom step's inputs using the `inputs` listener argument of type `dict`.

Refer to [the module document](https://docs.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn about the available listener arguments.

```python
# This sample custom step formats an input and outputs it
@app.function("sample_custom_step")
def sample_step_callback(inputs: dict, fail: Fail, complete: Complete):
    try:
        message = inputs["message"]
        complete(
            outputs={
                "message": f":wave: You submitted the following message: \n\n>{message}"
            }
        )
    except Exception as e:
        fail(f"Failed to handle a custom step request (error: {e})")
        raise e
```

<details>
<summary>
Example app manifest definition
</summary>

```json
...
"functions": {
    "sample_custom_step": {
        "title": "Sample custom step",
        "description": "Run a sample custom step",
        "input_parameters": {
            "message": {
                "type": "string",
                "title": "Message",
                "description": "A message to be formatted by the custom step",
                "is_required": true,
            }
        },
        "output_parameters": {
            "message": {
                "type": "string",
                "title": "Messge",
                "description": "A formatted message",
                "is_required": true,
            }
        }
    }
}
```

</details>

---

### Listening to custom step interactivity events

Your app's custom steps may create interactivity points for users, for example: Post a message with a button.

If such interaction points originate from a custom step execution, the events sent to your app representing the end-user interaction with these points are considered to be _function-scoped interactivity events_. These interactivity events can be handled by your app using the same concepts we covered earlier, such as [Listening to actions](/bolt-python/concepts/action-listening).

_function-scoped interactivity events_ will contain data related to the custom step (`function_executed` event) they were spawned from, such as custom step `inputs` and access to `complete()` and `fail()` listener arguments.

Your app can skip calling `complete()` or `fail()` in the `function()` handler method if the custom step creates an interaction point that requires user interaction before the step can end. However, in the relevant interactivity handler method, your app must invoke `complete()` or `fail()` to notify Slack that the custom step has been processed.

You’ll notice in all interactivity handler examples, `ack()` is used. It is required to call the `ack()` function within an interactivity listener to acknowledge that the request was received from Slack. This is discussed in the [acknowledging requests section](/bolt-python/concepts/acknowledge).

```python
# This sample custom step posts a message with a button
@app.function("custom_step_button")
def sample_step_callback(inputs, say, fail):
    try:
        say(
            channel=inputs["user_id"],  # sending a DM to this user
            text="Click the button to signal the step completion",
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Click the button to signal step completion"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Complete step"},
                        "action_id": "sample_click",
                    },
                }
            ],
        )
    except Exception as e:
        fail(f"Failed to handle a function request (error: {e})")

# Your listener will be called every time a block element with the action_id "sample_click" is triggered
@app.action("sample_click")
def handle_sample_click(ack, body, context, client, complete, fail):
    ack()
    try:
        # Since the button no longer works, we should remove it
        client.chat_update(
            channel=context.channel_id,
            ts=body["message"]["ts"],
            text="Congrats! You clicked the button",
        )

        # Signal that the custom step completed successfully
        complete({"user_id": context.actor_user_id})
    except Exception as e:
        fail(f"Failed to handle a function request (error: {e})")
```

<details>
<summary>
Example app manifest definition
</summary>

```json
...
"functions": {
    "custom_step_button": {
        "title": "Custom step with a button",
        "description": "Custom step that waits for a button click",
        "input_parameters": {
            "user_id": {
                "type": "slack#/types/user_id",
                "title": "User",
                "description": "The recipient of a message with a button",
                "is_required": true,
            }
        },
        "output_parameters": {
            "user_id": {
                "type": "slack#/types/user_id",
                "title": "User",
                "description": "The user that completed the function",
                "is_required": true
            }
        }
    }
}
```

</details>

Learn more about responding to interactivity, see the [Slack API documentation](/interactivity/handling-user-interaction).
