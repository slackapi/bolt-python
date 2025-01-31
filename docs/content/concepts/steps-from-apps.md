---
title: Steps from apps
lang: en
slug: /legacy/steps-from-apps
---

:::danger

Steps from apps are a deprecated feature.

Steps from apps are different than, and not interchangeable with, Slack automation workflows. We encourage those who are currently publishing steps from apps to consider the new [Slack automation features](https://api.slack.com/automation), such as [custom steps for Bolt](https://api.slack.com/automation/functions/custom-bolt),

Please [read the Slack API changelog entry](https://api.slack.com/changelog/2023-08-workflow-steps-from-apps-step-back) for more information.

:::

Steps from apps allow your app to create and process steps that users can add using [Workflow Builder](https://api.slack.com/workflows).

Steps from apps are made up of three distinct user events:

- Adding or editing the step in a Workflow
- Saving or updating the step's configuration
- The end user's execution of the step

All three events must be handled for a step from app to function.

Read more about steps from apps in the [API documentation](https://api.slack.com/workflows/steps).

## Creating steps from apps

To create a step from app, Bolt provides the `WorkflowStep` class.

When instantiating a new `WorkflowStep`, pass in the step's `callback_id` and a configuration object.

The configuration object contains three keys: `edit`, `save`, and `execute`. Each of these keys must be a single callback or a list of callbacks. All callbacks have access to a `step` object that contains information about the step from app event.

After instantiating a `WorkflowStep`, you can pass it into `app.step()`. Behind the scenes, your app will listen and respond to the step’s events using the callbacks provided in the configuration object.

Alternatively, steps from apps can also be created using the `WorkflowStepBuilder` class alongside a decorator pattern. For more information, including an example of this approach, [refer to the documentation](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/step.html#slack_bolt.workflows.step.step.WorkflowStepBuilder).

Refer to the module documents ([common](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) / [step-specific](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html)) to learn the available arguments.

```python
import os
from slack_bolt import App
from slack_bolt.workflows.step import WorkflowStep

# Initiate the Bolt app as you normally would
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

def edit(ack, step, configure):
    pass

def save(ack, view, update):
    pass

def execute(step, complete, fail):
    pass

# Create a new WorkflowStep instance
ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)

# Pass Step to set up listeners
app.step(ws)
```

## Adding or editing steps from apps

When a builder adds (or later edits) your step in their workflow, your app will receive a [`workflow_step_edit` event](https://api.slack.com/reference/workflows/workflow_step_edit). The `edit` callback in your `WorkflowStep` configuration will be run when this event is received.

Whether a builder is adding or editing a step, you need to send them a [step from app configuration modal](https://api.slack.com/reference/workflows/configuration-view). This modal is where step-specific settings are chosen, and it has more restrictions than typical modals—most notably, it cannot include `title`, `submit`, or `close` properties. By default, the configuration modal's `callback_id` will be the same as the step from app.

Within the `edit` callback, the `configure()` utility can be used to easily open your step's configuration modal by passing in the view's blocks with the corresponding `blocks` argument. To disable saving the configuration before certain conditions are met, you can also pass in `submit_disabled` with a value of `True`.

To learn more about opening configuration modals, [read the documentation](https://api.slack.com/workflows/steps#handle_config_view).

Refer to the module documents ([common](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) / [step-specific](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html)) to learn the available arguments.

```python
def edit(ack, step, configure):
    ack()

    blocks = [
        {
            "type": "input",
            "block_id": "task_name_input",
            "element": {
                "type": "plain_text_input",
                "action_id": "name",
                "placeholder": {"type": "plain_text", "text": "Add a task name"},
            },
            "label": {"type": "plain_text", "text": "Task name"},
        },
        {
            "type": "input",
            "block_id": "task_description_input",
            "element": {
                "type": "plain_text_input",
                "action_id": "description",
                "placeholder": {"type": "plain_text", "text": "Add a task description"},
            },
            "label": {"type": "plain_text", "text": "Task description"},
        },
    ]
    configure(blocks=blocks)

ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
app.step(ws)
```

## Saving step configurations

After the configuration modal is opened, your app will listen for the `view_submission` event. The `save` callback in your `WorkflowStep` configuration will be run when this event is received.

Within the `save` callback, the `update()` method can be used to save the builder's step configuration by passing in the following arguments:

- `inputs` is a dictionary representing the data your app expects to receive from the user upon step execution.
- `outputs` is a list of objects containing data that your app will provide upon the step's completion. Outputs can then be used in subsequent steps of the workflow.
- `step_name` overrides the default Step name
- `step_image_url` overrides the default Step image

To learn more about how to structure these parameters, [read the documentation](https://api.slack.com/reference/workflows/workflow_step).

Refer to the module documents ([common](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) / [step-specific](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html)) to learn the available arguments.

```python
def save(ack, view, update):
    ack()

    values = view["state"]["values"]
    task_name = values["task_name_input"]["name"]
    task_description = values["task_description_input"]["description"]
                
    inputs = {
        "task_name": {"value": task_name["value"]},
        "task_description": {"value": task_description["value"]}
    }
    outputs = [
        {
            "type": "text",
            "name": "task_name",
            "label": "Task name",
        },
        {
            "type": "text",
            "name": "task_description",
            "label": "Task description",
        }
    ]
    update(inputs=inputs, outputs=outputs)

ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
app.step(ws)
```

## Executing steps from app

When your step from app is executed by an end user, your app will receive a [`workflow_step_execute` event](https://api.slack.com/events/workflow_step_execute). The `execute` callback in your `WorkflowStep` configuration will be run when this event is received.

Using the `inputs` from the `save` callback, this is where you can make third-party API calls, save information to a database, update the user's Home tab, or decide the outputs that will be available to subsequent steps from apps by mapping values to the `outputs` object.

Within the `execute` callback, your app must either call `complete()` to indicate that the step's execution was successful, or `fail()` to indicate that the step's execution failed.

Refer to the module documents ([common](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html) / [step-specific](https://tools.slack.dev/bolt-python/api-docs/slack_bolt/workflows/step/utilities/index.html)) to learn the available arguments.

```python
def execute(step, complete, fail):
    inputs = step["inputs"]
    # if everything was successful
    outputs = {
        "task_name": inputs["task_name"]["value"],
        "task_description": inputs["task_description"]["value"],
    }
    complete(outputs=outputs)

    # if something went wrong
    error = {"message": "Just testing step failure!"}
    fail(error=error)

ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
app.step(ws)
```
