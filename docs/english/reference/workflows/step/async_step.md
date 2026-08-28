---
sidebar_label: async_step
title: slack_bolt.workflows.step.async_step
---

## `AsyncWorkflowStep`

```python
AsyncWorkflowStep(*, callback_id, edit, save, execute, app_name=None, base_logger=None)
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

**Parameters:**

- **callback_id** (Union[str, Pattern]) – The callback_id for this step from app
- **edit** (Union[Callable..., [Awaitable[BoltResponse]], AsyncListener, Sequence[Callable]]) – Either a single function or a list of functions for opening a modal in the builder UI
When it's a list, the first one is responsible for ack() while the rest are lazy listeners.
- **save** (Union[Callable..., [Awaitable[BoltResponse]], AsyncListener, Sequence[Callable]]) – Either a single function or a list of functions for handling modal interactions in the builder UI
When it's a list, the first one is responsible for ack() while the rest are lazy listeners.
- **execute** (Union[Callable..., [Awaitable[BoltResponse]], AsyncListener, Sequence[Callable]]) – Either a single function or a list of functions for handling steps from apps executions
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
edit: AsyncListener = self.build_listener(callback_id=callback_id, app_name=app_name, listener_or_functions=edit, name='edit', base_logger=base_logger)
```

`edit` listener, which displays a modal in Workflow Builder

### `execute`

```python
execute: AsyncListener = self.build_listener(callback_id=callback_id, app_name=app_name, listener_or_functions=execute, name='execute', base_logger=base_logger)
```

`execute` listener, which processes the step from app execution

### `save`

```python
save: AsyncListener = self.build_listener(callback_id=callback_id, app_name=app_name, listener_or_functions=save, name='save', base_logger=base_logger)
```

`save` listener, which accepts workflow creator's data submission in Workflow Builder

## `AsyncWorkflowStepBuilder`

```python
AsyncWorkflowStepBuilder(callback_id, app_name=None, base_logger=None)
```

Steps from apps.

Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details.

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

This builder is supposed to be used as decorator.

```python
my_step = AsyncWorkflowStep.builder("my_step")
@my_step.edit
async def edit_my_step(ack, configure):
    pass
@my_step.save
async def save_my_step(ack, step, update):
    pass
@my_step.execute
async def execute_my_step(step, complete, fail):
    pass
app.step(my_step)
```

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Parameters:**

- **callback_id** (Union[str, Pattern]) – The callback_id for the workflow
- **app_name** (Optional[str]) – The application name mainly for logging
- **base_logger** (Optional[Logger]) – The base logger

### `build`

```python
build(base_logger=None)
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Constructs a WorkflowStep object. This method may raise an exception
if the builder doesn't have enough configurations to build the object.

**Returns:**

- AsyncWorkflowStep – An `AsyncWorkflowStep` object

### `edit`

```python
edit(*args, matchers=None, middleware=None, lazy=None)
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new edit listener with details.

You can use this method as decorator as well.

```python
@my_step.edit
def edit_my_step(ack, configure):
    pass
```

It's also possible to add additional listener matchers and/or middleware

```python
@my_step.edit(matchers=[is_valid], middleware=[update_context])
def edit_my_step(ack, configure):
    pass
```

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Parameters:**

- ***args** – This method can behave as either decorator or a method
- **matchers** (Optional[Union[Callable..., [Awaitable[bool]], AsyncListenerMatcher]]) – Listener matchers
- **middleware** (Optional[Union[Callable, AsyncMiddleware]]) – Listener middleware
- **lazy** (Optional[List[Callable..., [Awaitable[None]]]]) – Lazy listeners

### `execute`

```python
execute(*args, matchers=None, middleware=None, lazy=None)
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new execute listener with details.

You can use this method as decorator as well.

```python
@my_step.execute
def execute_my_step(step, complete, fail):
    pass
```

It's also possible to add additional listener matchers and/or middleware

```python
@my_step.save(matchers=[is_valid], middleware=[update_context])
def execute_my_step(step, complete, fail):
    pass
```

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Parameters:**

- ***args** – This method can behave as either decorator or a method
- **matchers** (Optional[Union[Callable..., [Awaitable[bool]], AsyncListenerMatcher]]) – Listener matchers
- **middleware** (Optional[Union[Callable, AsyncMiddleware]]) – Listener middleware
- **lazy** (Optional[List[Callable..., [Awaitable[None]]]]) – Lazy listeners

### `save`

```python
save(*args, matchers=None, middleware=None, lazy=None)
```

Deprecated: Steps from apps for legacy workflows are now deprecated.

Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new save listener with details.

You can use this method as decorator as well.

```python
@my_step.save
def save_my_step(ack, step, update):
    pass
```

It's also possible to add additional listener matchers and/or middleware

```python
@my_step.save(matchers=[is_valid], middleware=[update_context])
def save_my_step(ack, step, update):
    pass
```

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Parameters:**

- ***args** – This method can behave as either decorator or a method
- **matchers** (Optional[Union[Callable..., [Awaitable[bool]], AsyncListenerMatcher]]) – Listener matchers
- **middleware** (Optional[Union[Callable, AsyncMiddleware]]) – Listener middleware
- **lazy** (Optional[List[Callable..., [Awaitable[None]]]]) – Lazy listeners
