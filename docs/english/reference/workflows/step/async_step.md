---
sidebar_label: async_step
title: slack_bolt.workflows.step.async_step
---

## AsyncBoltContext Objects

```python
class AsyncBoltContext(BaseContext)
```

Context object associated with a request from Slack.

#### to\_copyable

```python
def to_copyable() -> "AsyncBoltContext"
```

#### listener\_runner

```python
@property
def listener_runner() -> "AsyncioListenerRunner"
```

The properly configured listener_runner that is available for middleware/listeners.

#### client

```python
@property
def client() -> AsyncWebClient
```

The `AsyncWebClient` instance available for this request.

```python
    @app.event("app_mention")
    async def handle_events(context):
        await context.client.chat_postMessage(
            channel=context.channel_id,
            text="Thanks!",
        )

    # You can access "client" this way too.
    @app.event("app_mention")
    async def handle_events(client, context):
        await client.chat_postMessage(
            channel=context.channel_id,
            text="Thanks!",
        )
```

**Returns**:

  `AsyncWebClient` instance

#### ack

```python
@property
def ack() -> AsyncAck
```

`ack()` function for this request.

```python
    @app.action("button")
    async def handle_button_clicks(context):
        await context.ack()

    # You can access "ack" this way too.
    @app.action("button")
    async def handle_button_clicks(ack):
        await ack()
```

**Returns**:

  Callable `ack()` function

#### say

```python
@property
def say() -> AsyncSay
```

`say()` function for this request.

```python
    @app.action("button")
    async def handle_button_clicks(context):
        await context.ack()
        await context.say("Hi!")

    # You can access "ack" this way too.
    @app.action("button")
    async def handle_button_clicks(ack, say):
        await ack()
        await say("Hi!")
```

**Returns**:

  Callable `say()` function

#### respond

```python
@property
def respond() -> Optional[AsyncRespond]
```

`respond()` function for this request.

```python
    @app.action("button")
    async def handle_button_clicks(context):
        await context.ack()
        await context.respond("Hi!")

    # You can access "ack" this way too.
    @app.action("button")
    async def handle_button_clicks(ack, respond):
        await ack()
        await respond("Hi!")
```

**Returns**:

  Callable `respond()` function

#### complete

```python
@property
def complete() -> AsyncComplete
```

`complete()` function for this request. Once a custom function&#x27;s state is set to complete,
any outputs the function returns will be passed along to the next step of its housing workflow,
or complete the workflow if the function is the last step in a workflow. Additionally,
any interactivity handlers associated to a function invocation will no longer be invocable.

```python
    @app.function("reverse")
    async def handle_button_clicks(ack, complete):
        await ack()
        await complete(outputs={"stringReverse":"olleh"})

    @app.function("reverse")
    async def handle_button_clicks(context):
        await context.ack()
        await context.complete(outputs={"stringReverse":"olleh"})
```

**Returns**:

  Callable `complete()` function

#### fail

```python
@property
def fail() -> AsyncFail
```

`fail()` function for this request. Once a custom function&#x27;s state is set to error,
its housing workflow will be interrupted and any provided error message will be passed
on to the end user through SlackBot. Additionally, any interactivity handlers associated
to a function invocation will no longer be invocable.

```python
    @app.function("reverse")
    async def handle_button_clicks(ack, fail):
        await ack()
        await fail(error="something went wrong")

    @app.function("reverse")
    async def handle_button_clicks(context):
        await context.ack()
        await context.fail(error="something went wrong")
```

**Returns**:

  Callable `fail()` function

#### set\_title

```python
@property
def set_title() -> Optional[AsyncSetTitle]
```

#### set\_status

```python
@property
def set_status() -> Optional[AsyncSetStatus]
```

#### set\_suggested\_prompts

```python
@property
def set_suggested_prompts() -> Optional[AsyncSetSuggestedPrompts]
```

#### get\_thread\_context

```python
@property
def get_thread_context() -> Optional[AsyncGetThreadContext]
```

#### say\_stream

```python
@property
def say_stream() -> Optional[AsyncSayStream]
```

#### save\_thread\_context

```python
@property
def save_thread_context() -> Optional[AsyncSaveThreadContext]
```

## AsyncListener Objects

```python
class AsyncListener(metaclass=ABCMeta)
```

#### matchers: `Sequence[AsyncListenerMatcher]`

#### middleware: `Sequence[AsyncMiddleware]`

#### ack\_function: `Callable[..., Awaitable[BoltResponse]]`

#### lazy\_functions: `Sequence[Callable[..., Awaitable[None]]]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

#### async\_matches

```python
async def async_matches(*, req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

#### run\_async\_middleware

```python
async def run_async_middleware(
        *, req: AsyncBoltRequest,
        resp: BoltResponse) -> Tuple[Optional[BoltResponse], bool]
```

Runs an async middleware.

**Arguments**:

- `req` - The incoming request
- `resp` - The current response
  

**Returns**:

  A tuple of the processed response and a flag indicating termination

#### run\_ack\_function

```python
@abstractmethod
async def run_ack_function(*, request: AsyncBoltRequest,
                           response: BoltResponse) -> Optional[BoltResponse]
```

Runs all the registered middleware and then run the listener function.

**Arguments**:

- `request` - The incoming request
- `response` - The current response
  

**Returns**:

  The processed response

## AsyncCustomListener Objects

```python
class AsyncCustomListener(AsyncListener)
```

#### app\_name: `str`

#### ack\_function: `Callable[..., Awaitable[Optional[BoltResponse]]]`

type: ignore[assignment]

#### lazy\_functions: `Sequence[Callable[..., Awaitable[None]]]`

#### matchers: `Sequence[AsyncListenerMatcher]`

#### middleware: `Sequence[AsyncMiddleware]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             ack_function: Callable[..., Awaitable[Optional[BoltResponse]]],
             lazy_functions: Sequence[Callable[..., Awaitable[None]]],
             matchers: Sequence[AsyncListenerMatcher],
             middleware: Sequence[AsyncMiddleware],
             auto_acknowledgement: bool = False,
             ack_timeout: int = 3,
             base_logger: Optional[Logger] = None)
```

#### run\_ack\_function

```python
async def run_ack_function(*, request: AsyncBoltRequest,
                           response: BoltResponse) -> Optional[BoltResponse]
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

## AsyncCustomMiddleware Objects

```python
class AsyncCustomMiddleware(AsyncMiddleware)
```

#### app\_name: `str`

#### func: `Callable[..., Awaitable[Any]]`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             func: Callable[..., Awaitable[Any]],
             base_logger: Optional[Logger] = None)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

#### name

```python
@property
def name() -> str
```

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

## AsyncComplete Objects

```python
class AsyncComplete()
```

`complete()` utility to tell Slack the completion of a step from app execution.

```python
    async def execute(step, complete, fail):
        inputs = step["inputs"]
        # if everything was successful
        outputs = {
            "task_name": inputs["task_name"]["value"],
            "task_description": inputs["task_description"]["value"],
        }
        await complete(outputs=outputs)

    ws = AsyncWorkflowStep(
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
def __init__(*, client: AsyncWebClient, body: dict)
```

## AsyncConfigure Objects

```python
class AsyncConfigure()
```

`configure()` utility to send the modal view in Workflow Builder.

```python
    async def edit(ack, step, configure):
        await ack()

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
        await configure(blocks=blocks)

    ws = AsyncWorkflowStep(
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
def __init__(*, callback_id: str, client: AsyncWebClient, body: dict)
```

## AsyncFail Objects

```python
class AsyncFail()
```

`fail()` utility to tell Slack the execution failure of a step from app.

```python
    async def execute(step, complete, fail):
        inputs = step["inputs"]
        # if something went wrong
        error = {"message": "Just testing step failure!"}
        await fail(error=error)

    ws = AsyncWorkflowStep(
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
def __init__(*, client: AsyncWebClient, body: dict)
```

## AsyncUpdate Objects

```python
class AsyncUpdate()
```

`update()` utility to tell Slack the processing results of a `save` listener.

```python
    async def save(ack, view, update):
        await ack()

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
        await update(inputs=inputs, outputs=outputs)

    ws = AsyncWorkflowStep(
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
def __init__(*, client: AsyncWebClient, body: dict)
```

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

## AsyncListenerMatcher Objects

```python
class AsyncListenerMatcher(metaclass=ABCMeta)
```

#### async\_matches

```python
@abstractmethod
async def async_matches(req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` - The request
- `resp` - The response
  

**Returns**:

  True if matched

## AsyncCustomListenerMatcher Objects

```python
class AsyncCustomListenerMatcher(AsyncListenerMatcher)
```

#### app\_name: `str`

#### func: `Callable[..., Awaitable[bool]]`

#### arg\_names: `Sequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             func: Callable[..., Awaitable[bool]],
             base_logger: Optional[Logger] = None)
```

#### async\_matches

```python
async def async_matches(req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

## AsyncMiddleware Objects

```python
class AsyncMiddleware(metaclass=ABCMeta)
```

A middleware can process request data before other middleware and listener functions.

#### async\_process

```python
@abstractmethod
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

```python
    @app.middleware
    async def simple_middleware(req, resp, next):
        # do something here
        await next()
```

This `async_process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
    @app.middleware
    async def simple_middleware(req, resp, next_):
        # do something here
        await next_()
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

## AsyncWorkflowStepBuilder Objects

```python
class AsyncWorkflowStepBuilder()
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

**Arguments**:

- `callback_id` - The callback_id for the workflow
- `app_name` - The application name mainly for logging
- `base_logger` - The base logger

#### edit

```python
def edit(*args,
         matchers: Optional[Union[Callable[..., Awaitable[bool]],
                                  AsyncListenerMatcher]] = None,
         middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
         lazy: Optional[List[Callable[..., Awaitable[None]]]] = None)
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

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### save

```python
def save(*args,
         matchers: Optional[Union[Callable[..., Awaitable[bool]],
                                  AsyncListenerMatcher]] = None,
         middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
         lazy: Optional[List[Callable[..., Awaitable[None]]]] = None)
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

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### execute

```python
def execute(*args,
            matchers: Optional[Union[Callable[..., Awaitable[bool]],
                                     AsyncListenerMatcher]] = None,
            middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
            lazy: Optional[List[Callable[..., Awaitable[None]]]] = None)
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

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### build

```python
def build(base_logger: Optional[Logger] = None) -> "AsyncWorkflowStep"
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Constructs a WorkflowStep object. This method may raise an exception
if the builder doesn&#x27;t have enough configurations to build the object.

**Returns**:

  An `AsyncWorkflowStep` object

#### to\_listener\_matchers

```python
@staticmethod
def to_listener_matchers(
    app_name: str, matchers: Optional[List[Union[Callable[...,
                                                          Awaitable[bool]],
                                                 AsyncListenerMatcher]]]
) -> List[AsyncListenerMatcher]
```

#### to\_listener\_middleware

```python
@staticmethod
def to_listener_middleware(
    app_name: str, middleware: Optional[List[Union[Callable, AsyncMiddleware]]]
) -> List[AsyncMiddleware]
```

## AsyncWorkflowStep Objects

```python
class AsyncWorkflowStep()
```

#### callback\_id: `Union[str, Pattern]`

The Callback ID of the step from app

#### edit: `AsyncListener`

`edit` listener, which displays a modal in Workflow Builder

#### save: `AsyncListener`

`save` listener, which accepts workflow creator&#x27;s data submission in Workflow Builder

#### execute: `AsyncListener`

`execute` listener, which processes the step from app execution

#### \_\_init\_\_

```python
def __init__(*,
             callback_id: Union[str, Pattern],
             edit: Union[Callable[..., Awaitable[BoltResponse]], AsyncListener,
                         Sequence[Callable]],
             save: Union[Callable[..., Awaitable[BoltResponse]], AsyncListener,
                         Sequence[Callable]],
             execute: Union[Callable[..., Awaitable[BoltResponse]],
                            AsyncListener, Sequence[Callable]],
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
- `execute` - Either a single function or a list of functions for handling steps from apps executions
  When it&#x27;s a list, the first one is responsible for ack() while the rest are lazy listeners.
- `app_name` - The app name that can be mainly used for logging
- `base_logger` - The logger instance that can be used as a template when creating this step&#x27;s logger

#### builder

```python
@classmethod
def builder(cls,
            callback_id: Union[str, Pattern],
            base_logger: Optional[Logger] = None) -> AsyncWorkflowStepBuilder
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
                   listener_or_functions: Union[AsyncListener, Callable,
                                                List[Callable]],
                   name: str,
                   matchers: Optional[List[AsyncListenerMatcher]] = None,
                   middleware: Optional[List[AsyncMiddleware]] = None,
                   base_logger: Optional[Logger] = None)
```

