---
sidebar_label: step
title: slack_bolt.workflows.step
---

## Submodules

- [slack_bolt.workflows.step.async_step](/tools/bolt-python/reference/workflows/step/async_step)
- [slack_bolt.workflows.step.async_step_middleware](/tools/bolt-python/reference/workflows/step/async_step_middleware)
- [slack_bolt.workflows.step.internals](/tools/bolt-python/reference/workflows/step/internals)
- [slack_bolt.workflows.step.step](/tools/bolt-python/reference/workflows/step/step)
- [slack_bolt.workflows.step.step_middleware](/tools/bolt-python/reference/workflows/step/step_middleware)
- [slack_bolt.workflows.step.utilities](/tools/bolt-python/reference/workflows/step/utilities)

## WorkflowStep Objects

```python
class WorkflowStep()
```

#### callback\_id: `Union[str, Pattern]`

The Callback ID of the step from app

#### edit: `Listener`

`edit` listener, which displays a modal in Workflow Builder

#### save: `Listener`

`save` listener, which accepts workflow creator's data submission in Workflow Builder

#### execute: `Listener`

`execute` listener, which processes step from app execution

#### \_\_init\_\_

```python
def __init__(
    *,
    callback_id: Union[str, Pattern],
    edit: Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]],
    save: Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]],
    execute: Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]],
    app_name: Optional[str] = None,
    base_logger: Optional[Logger] = None)
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

**Arguments**:

- `callback_id` _Union[str, Pattern]_ - The callback_id for this step from app
- `edit` _Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]]_ - Either a single function or a list of functions for opening a modal in the builder UI
  When it's a list, the first one is responsible for ack() while the rest are lazy listeners.
- `save` _Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]]_ - Either a single function or a list of functions for handling modal interactions in the builder UI
  When it's a list, the first one is responsible for ack() while the rest are lazy listeners.
- `execute` _Union[Callable[..., Optional[BoltResponse]], Listener, Sequence[Callable]]_ - Either a single function or a list of functions for handling step from app executions
  When it's a list, the first one is responsible for ack() while the rest are lazy listeners.
- `app_name` _Optional[str]_ - The app name that can be mainly used for logging
- `base_logger` _Optional[Logger]_ - The logger instance that can be used as a template when creating this step's logger

#### builder

```python
def builder(
    callback_id: Union[str, Pattern],
    base_logger: Optional[Logger] = None) -> WorkflowStepBuilder
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

#### build\_listener

```python
def build_listener(
    callback_id: Union[str, Pattern],
    app_name: str,
    listener_or_functions: Union[Listener, Callable, List[Callable]],
    name: str,
    matchers: Optional[List[ListenerMatcher]] = None,
    middleware: Optional[List[Middleware]] = None,
    base_logger: Optional[Logger] = None) -> Listener
```

## WorkflowStepMiddleware Objects

```python
class WorkflowStepMiddleware(Middleware)
```

Base middleware for step from app specific ones.

#### \_\_init\_\_

```python
def __init__(step: WorkflowStep)
```

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

## Complete Objects

```python
class Complete()
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

#### \_\_init\_\_

```python
def __init__(*, client: WebClient, body: dict)
```

## Configure Objects

```python
class Configure()
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

#### \_\_init\_\_

```python
def __init__(*, callback_id: str, client: WebClient, body: dict)
```

## Update Objects

```python
class Update()
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

#### \_\_init\_\_

```python
def __init__(*, client: WebClient, body: dict)
```

## Fail Objects

```python
class Fail()
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

#### \_\_init\_\_

```python
def __init__(*, client: WebClient, body: dict)
```
