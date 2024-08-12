---
title: Listening and responding to custom steps
lang: en
slug: /concepts/custom-steps
---

Your app can use the `function()` method to listen to incoming [custom step requests](https://api.slack.com/automation/functions/custom-bolt). The method requires a step `callback_id` of type `str`. This `callback_id` must also be defined in your [Function](https://api.slack.com/concepts/manifests#functions) definition. Custom steps must be finalized using the `complete()` or `fail()` listener arguments to notify Slack that your app has processed the request.

* `complete()` requires **one** argument: `outputs` of type `dict`. It completes your custom step **successfully** and provides a dictionary containing the outputs of your custom step as per its definition.
* `fail` requires **one** argument: `error` of type `str`. It completes your custom step **unsuccessfully** and provides a message containing information regarding why your custom step failed.

You can reference your custom step's inputs using the `inputs` listener argument of type `dict`.

Refer to [the module document](https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) to learn about the available listener arguments.

```python
# This sample custom step formats an input and outputs it
@app.function("sample_custom_step")
def sample_step_callback(inputs: dict, ack: Ack, fail: Fail, complete: Complete):
    try:
        ack()
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
  Listening to custom step actions
  </summary>
  Your app can listen to user actions, like button clicks, created from `custom steps` using the `action` method.
  
  Actions can be filtered on an `action_id` of type `str` or `re.Pattern`. `action_id`s act as unique identifiers for interactive components on the Slack platform.

  Your app can skip calling `complete()` or `fail()` in the `function()` method if the custom step creates an `action` that waits for user interaction. However, in the `action()` method, your app must invoke `complete()` or `fail()` to notify Slack that the custom step has been processed.

```python
# This sample custom step posts a message with a button
@app.function("custom_step_button")
def sample_step_callback(inputs: dict, say: Say, fail: Fail):
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
def handle_sample_click(
    ack: Ack, body: dict, context: BoltContext, client: WebClient, complete: Complete, fail: Fail
):
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

</details>
