---
sidebar_label: step
title: slack_bolt.workflows.step
---

## `Complete`

```python
Complete(*, client, body)
```

`complete()` utility to tell Slack the completion of a step from app execution.

```python
def execute(step, complete, fail):
    inputs = step["inputs"]
    # if everything was successful
    outputs = {
        "task_name": inputs["task_name"]["value"],
        "task_description": inputs["task_description"]["value"],
    }
    complete(outputs=outputs)

ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)
app.step(ws)
```

This utility is a thin wrapper of workflows.stepCompleted API method.
Refer to https://api.slack.com/methods/workflows.stepCompleted for details.

## `Configure`

```python
Configure(*, callback_id, client, body)
```

`configure()` utility to send the modal view in Workflow Builder.

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

Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details.

## `Fail`

```python
Fail(*, client, body)
```

`fail()` utility to tell Slack the execution failure of a step from app.

```python
def execute(step, complete, fail):
    inputs = step["inputs"]
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

This utility is a thin wrapper of workflows.stepFailed API method.
Refer to https://api.slack.com/methods/workflows.stepFailed for details.

## `Update`

```python
Update(*, client, body)
```

`update()` utility to tell Slack the processing results of a `save` listener.

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

This utility is a thin wrapper of workflows.stepFailed API method.
Refer to https://api.slack.com/methods/workflows.updateStep for details.

## `WorkflowStep`

```python
WorkflowStep(*, callback_id, edit, save, execute, app_name=None, base_logger=None)
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

**Parameters:**

- **callback_id** (Union[str, Pattern]) – The callback_id for this step from app
- **edit** (Union[Callable..., [Optional[BoltResponse]], Listener, Sequence[Callable]]) – Either a single function or a list of functions for opening a modal in the builder UI
When it's a list, the first one is responsible for ack() while the rest are lazy listeners.
- **save** (Union[Callable..., [Optional[BoltResponse]], Listener, Sequence[Callable]]) – Either a single function or a list of functions for handling modal interactions in the builder UI
When it's a list, the first one is responsible for ack() while the rest are lazy listeners.
- **execute** (Union[Callable..., [Optional[BoltResponse]], Listener, Sequence[Callable]]) – Either a single function or a list of functions for handling step from app executions
When it's a list, the first one is responsible for ack() while the rest are lazy listeners.
- **app_name** (Optional[str]) – The app name that can be mainly used for logging
- **base_logger** (Optional[Logger]) – The logger instance that can be used as a template when creating this step's logger

### `builder`

```python
builder(callback_id, base_logger=None)
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

### `callback_id`

```python
callback_id: Union[str, Pattern] = callback_id
```

The Callback ID of the step from app

### `edit`

```python
edit: Listener = self.build_listener(callback_id=callback_id, app_name=app_name, listener_or_functions=edit, name='edit', base_logger=base_logger)
```

`edit` listener, which displays a modal in Workflow Builder

### `execute`

```python
execute: Listener = self.build_listener(callback_id=callback_id, app_name=app_name, listener_or_functions=execute, name='execute', base_logger=base_logger)
```

`execute` listener, which processes step from app execution

### `save`

```python
save: Listener = self.build_listener(callback_id=callback_id, app_name=app_name, listener_or_functions=save, name='save', base_logger=base_logger)
```

`save` listener, which accepts workflow creator's data submission in Workflow Builder

## `WorkflowStepMiddleware`

```python
WorkflowStepMiddleware(step)
```

Bases: Middleware

Base middleware for step from app specific ones.

### `name`

```python
name: str
```

The name of this middleware.

## Submodules

- [slack_bolt.workflows.step.async_step](/tools/bolt-python/reference/workflows/step/async_step)
- [slack_bolt.workflows.step.async_step_middleware](/tools/bolt-python/reference/workflows/step/async_step_middleware)
- [slack_bolt.workflows.step.internals](/tools/bolt-python/reference/workflows/step/internals)
- [slack_bolt.workflows.step.step](/tools/bolt-python/reference/workflows/step/step)
- [slack_bolt.workflows.step.step_middleware](/tools/bolt-python/reference/workflows/step/step_middleware)
- [slack_bolt.workflows.step.utilities](/tools/bolt-python/reference/workflows/step/utilities)
