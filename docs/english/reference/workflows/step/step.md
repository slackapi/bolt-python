---
sidebar_label: step
title: slack_bolt.workflows.step.step
slug: step
---

## BoltContext Objects

```python
class BoltContext(BaseContext)
```

Context object associated with a request from Slack.

#### to\_copyable

```python
def to_copyable() -> "BoltContext"
```

#### listener\_runner

```python
@property
def listener_runner() -> "ThreadListenerRunner"
```

The properly configured listener_runner that is available for middleware/listeners.

#### client

```python
@property
def client() -> WebClient
```

The `WebClient` instance available for this request.

```python
    @app.event("app_mention")
    def handle_events(context):
        context.client.chat_postMessage(
            channel=context.channel_id,
            text="Thanks!",
        )

    # You can access "client" this way too.
    @app.event("app_mention")
    def handle_events(client, context):
        client.chat_postMessage(
            channel=context.channel_id,
            text="Thanks!",
        )
```

**Returns**:

  `WebClient` instance

#### ack

```python
@property
def ack() -> Ack
```

`ack()` function for this request.

```python
    @app.action("button")
    def handle_button_clicks(context):
        context.ack()

    # You can access "ack" this way too.
    @app.action("button")
    def handle_button_clicks(ack):
        ack()
```

**Returns**:

  Callable `ack()` function

#### say

```python
@property
def say() -> Say
```

`say()` function for this request.

```python
    @app.action("button")
    def handle_button_clicks(context):
        context.ack()
        context.say("Hi!")

    # You can access "ack" this way too.
    @app.action("button")
    def handle_button_clicks(ack, say):
        ack()
        say("Hi!")
```

**Returns**:

  Callable `say()` function

#### respond

```python
@property
def respond() -> Optional[Respond]
```

`respond()` function for this request.

```python
    @app.action("button")
    def handle_button_clicks(context):
        context.ack()
        context.respond("Hi!")

    # You can access "ack" this way too.
    @app.action("button")
    def handle_button_clicks(ack, respond):
        ack()
        respond("Hi!")
```

**Returns**:

  Callable `respond()` function

#### complete

```python
@property
def complete() -> Complete
```

`complete()` function for this request. Once a custom function&#x27;s state is set to complete,
any outputs the function returns will be passed along to the next step of its housing workflow,
or complete the workflow if the function is the last step in a workflow. Additionally,
any interactivity handlers associated to a function invocation will no longer be invocable.

```python
    @app.function("reverse")
    def handle_button_clicks(ack, complete):
        ack()
        complete(outputs={"stringReverse":"olleh"})

    @app.function("reverse")
    def handle_button_clicks(context):
        context.ack()
        context.complete(outputs={"stringReverse":"olleh"})
```

**Returns**:

  Callable `complete()` function

#### fail

```python
@property
def fail() -> Fail
```

`fail()` function for this request. Once a custom function&#x27;s state is set to error,
its housing workflow will be interrupted and any provided error message will be passed
on to the end user through SlackBot. Additionally, any interactivity handlers associated
to a function invocation will no longer be invocable.

```python
    @app.function("reverse")
    def handle_button_clicks(ack, fail):
        ack()
        fail(error="something went wrong")

    @app.function("reverse")
    def handle_button_clicks(context):
        context.ack()
        context.fail(error="something went wrong")
```

**Returns**:

  Callable `fail()` function

#### set\_title

```python
@property
def set_title() -> Optional[SetTitle]
```

#### set\_status

```python
@property
def set_status() -> Optional[SetStatus]
```

#### set\_suggested\_prompts

```python
@property
def set_suggested_prompts() -> Optional[SetSuggestedPrompts]
```

#### get\_thread\_context

```python
@property
def get_thread_context() -> Optional[GetThreadContext]
```

#### say\_stream

```python
@property
def say_stream() -> Optional[SayStream]
```

#### save\_thread\_context

```python
@property
def save_thread_context() -> Optional[SaveThreadContext]
```

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

## Listener Objects

```python
class Listener(metaclass=ABCMeta)
```

#### matchers: `Sequence[ListenerMatcher]`

#### middleware: `Sequence[Middleware]`

#### ack\_function: `Callable[..., BoltResponse]`

#### lazy\_functions: `Sequence[Callable[..., None]]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

#### matches

```python
def matches(*, req: BoltRequest, resp: BoltResponse) -> bool
```

#### run\_middleware

```python
def run_middleware(*, req: BoltRequest,
                   resp: BoltResponse) -> Tuple[Optional[BoltResponse], bool]
```

Runs a middleware.

**Arguments**:

- `req` - The incoming request
- `resp` - The current response
  

**Returns**:

  A tuple of the processed response and a flag indicating termination

#### run\_ack\_function

```python
@abstractmethod
def run_ack_function(*, request: BoltRequest,
                     response: BoltResponse) -> Optional[BoltResponse]
```

Runs all the registered middleware and then run the listener function.

**Arguments**:

- `request` - The incoming request
- `response` - The current response
  

**Returns**:

  The processed response

## CustomListener Objects

```python
class CustomListener(Listener)
```

#### app\_name: `str`

#### ack\_function: `Callable[..., Optional[BoltResponse]]`

type: ignore[assignment]

#### lazy\_functions: `Sequence[Callable[..., None]]`

#### matchers: `Sequence[ListenerMatcher]`

#### middleware: `Sequence[Middleware]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             ack_function: Callable[..., Optional[BoltResponse]],
             lazy_functions: Sequence[Callable[..., None]],
             matchers: Sequence[ListenerMatcher],
             middleware: Sequence[Middleware],
             auto_acknowledgement: bool = False,
             ack_timeout: int = 3,
             base_logger: Optional[Logger] = None)
```

#### run\_ack\_function

```python
def run_ack_function(*, request: BoltRequest,
                     response: BoltResponse) -> Optional[BoltResponse]
```

## ListenerMatcher Objects

```python
class ListenerMatcher(metaclass=ABCMeta)
```

#### matches

```python
@abstractmethod
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` - The request
- `resp` - The response
  

**Returns**:

  True if matched.

## CustomListenerMatcher Objects

```python
class CustomListenerMatcher(ListenerMatcher)
```

#### app\_name: `str`

#### func: `Callable[..., bool]`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             func: Callable[..., bool],
             base_logger: Optional[Logger] = None)
```

#### matches

```python
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

#### workflow\_step\_edit

```python
def workflow_step_edit(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### workflow\_step\_save

```python
def workflow_step_save(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

#### workflow\_step\_execute

```python
def workflow_step_execute(
    callback_id: Union[str, Pattern],
    asyncio: bool = False,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

## CustomMiddleware Objects

```python
class CustomMiddleware(Middleware)
```

#### app\_name: `str`

#### func: `Callable[..., Any]`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             func: Callable,
             base_logger: Optional[Logger] = None)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

#### name

```python
@property
def name() -> str
```

## Middleware Objects

```python
class Middleware(metaclass=ABCMeta)
```

A middleware can process request data before other middleware and listener functions.

#### process

```python
@abstractmethod
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

```python
    @app.middleware
    def simple_middleware(req, resp, next):
        # do something here
        next()
```

This `process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
    @app.middleware
    def simple_middleware(req, resp, next_):
        # do something here
        next_()
```

**Arguments**:

- `req` - The incoming request
- `resp` - The response
- `next` - The function to tell the chain that it can continue
  

**Returns**:

  Processed response (optional)

#### name

```python
@property
def name() -> str
```

The name of this middleware

## BoltResponse Objects

```python
class BoltResponse()
```

#### status: `int`

HTTP status code

#### body: `str`

The response body (dict and str are supported)

#### headers: `Dict[str, Sequence[str]]`

The response headers.

#### \_\_init\_\_

```python
def __init__(*,
             status: int,
             body: Union[str, dict] = "",
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None)
```

The response from a Bolt app.

**Arguments**:

- `status` - HTTP status code
- `body` - The response body (dict and str are supported)
- `headers` - The response headers.

#### first\_headers

```python
def first_headers() -> Dict[str, str]
```

#### first\_headers\_without\_set\_cookie

```python
def first_headers_without_set_cookie() -> Dict[str, str]
```

#### cookies

```python
def cookies() -> Sequence[SimpleCookie]
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

## WorkflowStepBuilder Objects

```python
class WorkflowStepBuilder()
```

Steps from apps
Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details.

#### callback\_id: `Union[str, Pattern]`

The callback_id for the workflow

#### \_\_init\_\_

```python
def __init__(callback_id: Union[str, Pattern],
             app_name: Optional[str] = None,
             base_logger: Optional[Logger] = None)
```

Deprecated:
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

- `callback_id` - The callback_id for the workflow
- `app_name` - The application name mainly for logging
- `base_logger` - The base logger

#### edit

```python
def edit(*args,
         matchers: Optional[Union[Callable[..., bool],
                                  ListenerMatcher]] = None,
         middleware: Optional[Union[Callable, Middleware]] = None,
         lazy: Optional[List[Callable[..., None]]] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new edit listener with details.

You can use this method as decorator as well.

```python
    @my_step.edit
    def edit_my_step(ack, configure):
        pass
```

It&#x27;s also possible to add additional listener matchers and/or middleware

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
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### save

```python
def save(*args,
         matchers: Optional[Union[Callable[..., bool],
                                  ListenerMatcher]] = None,
         middleware: Optional[Union[Callable, Middleware]] = None,
         lazy: Optional[List[Callable[..., None]]] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new save listener with details.

You can use this method as decorator as well.

```python
    @my_step.save
    def save_my_step(ack, step, update):
        pass
```

It&#x27;s also possible to add additional listener matchers and/or middleware

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
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### execute

```python
def execute(*args,
            matchers: Optional[Union[Callable[..., bool],
                                     ListenerMatcher]] = None,
            middleware: Optional[Union[Callable, Middleware]] = None,
            lazy: Optional[List[Callable[..., None]]] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new execute listener with details.

You can use this method as decorator as well.

```python
    @my_step.execute
    def execute_my_step(step, complete, fail):
        pass
```

It&#x27;s also possible to add additional listener matchers and/or middleware

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
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### build

```python
def build(base_logger: Optional[Logger] = None) -> "WorkflowStep"
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Constructs a WorkflowStep object. This method may raise an exception
if the builder doesn&#x27;t have enough configurations to build the object.

**Returns**:

  WorkflowStep object

#### to\_listener\_matchers

```python
@staticmethod
def to_listener_matchers(
        app_name: str,
        matchers: Optional[List[Union[Callable[..., bool], ListenerMatcher]]],
        base_logger: Optional[Logger] = None) -> List[ListenerMatcher]
```

#### to\_listener\_middleware

```python
@staticmethod
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

`save` listener, which accepts workflow creator&#x27;s data submission in Workflow Builder

#### execute: `Listener`

`execute` listener, which processes step from app execution

#### \_\_init\_\_

```python
def __init__(*,
             callback_id: Union[str, Pattern],
             edit: Union[Callable[..., Optional[BoltResponse]], Listener,
                         Sequence[Callable]],
             save: Union[Callable[..., Optional[BoltResponse]], Listener,
                         Sequence[Callable]],
             execute: Union[Callable[..., Optional[BoltResponse]], Listener,
                            Sequence[Callable]],
             app_name: Optional[str] = None,
             base_logger: Optional[Logger] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

**Arguments**:

- `callback_id` - The callback_id for this step from app
- `edit` - Either a single function or a list of functions for opening a modal in the builder UI
  When it&#x27;s a list, the first one is responsible for ack() while the rest are lazy listeners.
- `save` - Either a single function or a list of functions for handling modal interactions in the builder UI
  When it&#x27;s a list, the first one is responsible for ack() while the rest are lazy listeners.
- `execute` - Either a single function or a list of functions for handling step from app executions
  When it&#x27;s a list, the first one is responsible for ack() while the rest are lazy listeners.
- `app_name` - The app name that can be mainly used for logging
- `base_logger` - The logger instance that can be used as a template when creating this step&#x27;s logger

#### builder

```python
@classmethod
def builder(cls,
            callback_id: Union[str, Pattern],
            base_logger: Optional[Logger] = None) -> WorkflowStepBuilder
```

Deprecated:
    Steps from apps for legacy workflows are now deprecated.
    Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

#### build\_listener

```python
@classmethod
def build_listener(cls,
                   callback_id: Union[str, Pattern],
                   app_name: str,
                   listener_or_functions: Union[Listener, Callable,
                                                List[Callable]],
                   name: str,
                   matchers: Optional[List[ListenerMatcher]] = None,
                   middleware: Optional[List[Middleware]] = None,
                   base_logger: Optional[Logger] = None) -> Listener
```

