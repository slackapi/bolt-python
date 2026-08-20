---
sidebar_label: step
title: slack_bolt.workflows.step.step
slug: step
---

## WorkflowStepBuilder Objects

```python
class WorkflowStepBuilder()
```

Steps from apps
Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details.

#### callback\_id: `Union[str, Pattern]`

#### \_\_init\_\_

```python
def __init__(
    callback_id: Union[str, Pattern],
    app_name: Optional[str] = None,
    base_logger: Optional[Logger] = None)
```

**Deprecated**:

Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

This builder is supposed to be used as decorator.

```python
my_step = WorkflowStep.builder("my_step")
@my_step.edit
def edit_my_step(ack, configure):
    pass
@my_step.save
def save_my_step(ack, step, update):
    pass
@my_step.execute
def execute_my_step(step, complete, fail):
    pass
app.step(my_step)
```

For further information about WorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `callback_id` _Union[str, Pattern]_ - The callback_id for the workflow
- `app_name` _Optional[str]_ - The application name mainly for logging
- `base_logger` _Optional[Logger]_ - The base logger

#### edit

```python
def edit(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

**Deprecated**:

Steps from apps for legacy workflows are now deprecated.
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

For further information about WorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` _Optional[Union[Callable[..., bool], ListenerMatcher]]_ - Listener matchers
- `middleware` _Optional[Union[Callable, Middleware]]_ - Listener middleware
- `lazy` _Optional[List[Callable[..., None]]]_ - Lazy listeners

#### save

```python
def save(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

**Deprecated**:

Steps from apps for legacy workflows are now deprecated.
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

For further information about WorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` _Optional[Union[Callable[..., bool], ListenerMatcher]]_ - Listener matchers
- `middleware` _Optional[Union[Callable, Middleware]]_ - Listener middleware
- `lazy` _Optional[List[Callable[..., None]]]_ - Lazy listeners

#### execute

```python
def execute(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

**Deprecated**:

Steps from apps for legacy workflows are now deprecated.
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

For further information about WorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` _Optional[Union[Callable[..., bool], ListenerMatcher]]_ - Listener matchers
- `middleware` _Optional[Union[Callable, Middleware]]_ - Listener middleware
- `lazy` _Optional[List[Callable[..., None]]]_ - Lazy listeners

#### build

```python
def build(base_logger: Optional[Logger] = None) -> WorkflowStep
```

**Deprecated**:

Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Constructs a WorkflowStep object. This method may raise an exception
if the builder doesn't have enough configurations to build the object.

**Returns**:

- `WorkflowStep` - WorkflowStep object

#### to\_listener\_matchers

```python
def to_listener_matchers(
    app_name: str,
    matchers: Optional[List[Union[Callable[..., bool], ListenerMatcher]]],
    base_logger: Optional[Logger] = None) -> List[ListenerMatcher]
```

#### to\_listener\_middleware

```python
def to_listener_middleware(
    app_name: str,
    middleware: Optional[List[Union[Callable, Middleware]]],
    base_logger: Optional[Logger] = None) -> List[Middleware]
```

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

**Deprecated**:

Steps from apps for legacy workflows are now deprecated.
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

**Deprecated**:

Steps from apps for legacy workflows are now deprecated.
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
