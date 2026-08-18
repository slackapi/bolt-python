---
sidebar_label: args
title: slack_bolt.kwargs_injection.args
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

## Ack Objects

```python
class Ack()
```

#### response: `Optional[BoltResponse]`

#### \_\_init\_\_

```python
def __init__()
```

## Complete Objects

```python
class Complete()
```

#### client: `WebClient`

#### function\_execution\_id: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(client: WebClient, function_execution_id: Optional[str])
```

#### has\_been\_called

```python
def has_been_called() -> bool
```

Check if this complete function has been called.

**Returns**:

- `bool` - True if the complete function has been called, False otherwise.

## Fail Objects

```python
class Fail()
```

#### client: `WebClient`

#### function\_execution\_id: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(client: WebClient, function_execution_id: Optional[str])
```

#### has\_been\_called

```python
def has_been_called() -> bool
```

Check if this fail function has been called.

**Returns**:

- `bool` - True if the fail function has been called, False otherwise.

## GetThreadContext Objects

```python
class GetThreadContext()
```

#### thread\_context\_store: `AssistantThreadContextStore`

#### payload: `dict`

#### channel\_id: `str`

#### thread\_ts: `str`

#### thread\_context\_loaded: `bool`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AssistantThreadContextStore,
             channel_id: str, thread_ts: str, payload: dict)
```

## Respond Objects

```python
class Respond()
```

#### response\_url: `Optional[str]`

#### proxy: `Optional[str]`

#### ssl: `Optional[SSLContext]`

#### \_\_init\_\_

```python
def __init__(*,
             response_url: Optional[str],
             proxy: Optional[str] = None,
             ssl: Optional[SSLContext] = None)
```

## SaveThreadContext Objects

```python
class SaveThreadContext()
```

#### thread\_context\_store: `AssistantThreadContextStore`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AssistantThreadContextStore,
             channel_id: str, thread_ts: str)
```

## Say Objects

```python
class Say()
```

#### client: `Optional[WebClient]`

#### channel: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### metadata: `Optional[Union[Dict, Metadata]]`

#### build\_metadata: `Optional[Callable[[], Optional[Union[Dict, Metadata]]]]`

#### \_\_init\_\_

```python
def __init__(
    client: Optional[WebClient],
    channel: Optional[str],
    thread_ts: Optional[str] = None,
    metadata: Optional[Union[Dict, Metadata]] = None,
    build_metadata: Optional[Callable[[], Optional[Union[Dict,
                                                         Metadata]]]] = None)
```

## SayStream Objects

```python
class SayStream()
```

#### client: `WebClient`

#### channel: `Optional[str]`

#### recipient\_team\_id: `Optional[str]`

#### recipient\_user\_id: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(*,
             client: WebClient,
             channel: Optional[str] = None,
             recipient_team_id: Optional[str] = None,
             recipient_user_id: Optional[str] = None,
             thread_ts: Optional[str] = None)
```

## SetStatus Objects

```python
class SetStatus()
```

#### client: `WebClient`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(client: WebClient, channel_id: str, thread_ts: str)
```

## SetSuggestedPrompts Objects

```python
class SetSuggestedPrompts()
```

#### client: `WebClient`

#### channel\_id: `str`

#### thread\_ts: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(client: WebClient,
             channel_id: str,
             thread_ts: Optional[str] = None)
```

## SetTitle Objects

```python
class SetTitle()
```

#### client: `WebClient`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(client: WebClient, channel_id: str, thread_ts: str)
```

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body: `str`

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### context: `BoltContext`

The context in this request.

#### lazy\_only: `bool`

#### lazy\_function\_name: `Optional[str]`

#### mode: `str`

The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

#### \_\_init\_\_

```python
def __init__(*,
             body: Union[str, dict],
             query: Optional[Union[str, Dict[str, str],
                                   Dict[str, Sequence[str]]]] = None,
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
             context: Optional[Dict[str, Any]] = None,
             mode: str = "http")
```

Request to a Bolt app.

**Arguments**:

- `body` - The raw request body (only plain text is supported for &quot;http&quot; mode)
- `query` - The query string data in any data format.
- `headers` - The request headers.
- `context` - The context in this request.
- `mode` - The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
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

## Args Objects

```python
class Args()
```

All the arguments in this class are available in any middleware / listeners.
You can inject the named variables in the argument list in arbitrary order.

```python
    @app.action("link_button")
    def handle_buttons(ack, respond, logger, context, body, client):
        logger.info(f"request body: {body}")
        ack()
        if context.channel_id is not None:
            respond("Hi!")
        client.views_open(
            trigger_id=body["trigger_id"],
            view={ ... }
        )
```

Alternatively, you can include a parameter named `args` and it will be injected with an instance of this class.

```python
    @app.action("link_button")
    def handle_buttons(args):
        args.logger.info(f"request body: {args.body}")
        args.ack()
        if args.context.channel_id is not None:
            args.respond("Hi!")
        args.client.views_open(
            trigger_id=args.body["trigger_id"],
            view={ ... }
        )
```

#### client: `WebClient`

`slack_sdk.web.WebClient` instance with a valid token

#### logger: `Logger`

Logger instance

#### req: `BoltRequest`

Incoming request from Slack

#### resp: `BoltResponse`

Response representation

#### request: `BoltRequest`

Incoming request from Slack

#### response: `BoltResponse`

Response representation

#### context: `BoltContext`

Context data associated with the incoming request

#### body: `Dict[str, Any]`

Parsed request body data

#### payload: `Dict[str, Any]`

The unwrapped core data in the request body

#### options: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.options` listener

#### shortcut: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.shortcut` listener

#### action: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.action` listener

#### view: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.view` listener

#### command: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.command` listener

#### event: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.event` listener

#### message: `Optional[Dict[str, Any]]`

An alias for payload in an `@app.message` listener

#### ack: `Ack`

`ack()` utility function, which returns acknowledgement to the Slack servers

#### say: `Say`

`say()` utility function, which calls `chat.postMessage` API with the associated channel ID

#### respond: `Respond`

`respond()` utility function, which utilizes the associated `response_url`

#### complete: `Complete`

`complete()` utility function, signals a successful completion of the custom function

#### fail: `Fail`

`fail()` utility function, signal that the custom function failed to complete

#### set\_status: `Optional[SetStatus]`

`set_status()` utility function for AI Agents &amp; Assistants

#### set\_title: `Optional[SetTitle]`

`set_title()` utility function for AI Agents &amp; Assistants

#### set\_suggested\_prompts: `Optional[SetSuggestedPrompts]`

`set_suggested_prompts()` utility function for AI Agents &amp; Assistants

#### get\_thread\_context: `Optional[GetThreadContext]`

`get_thread_context()` utility function for AI Agents &amp; Assistants

#### save\_thread\_context: `Optional[SaveThreadContext]`

`save_thread_context()` utility function for AI Agents &amp; Assistants

#### say\_stream: `Optional[SayStream]`

`say_stream()` utility function for conversations, AI Agents &amp; Assistants

#### next: `Callable[[], None]`

`next()` utility function, which tells the middleware chain that it can continue with the next one

#### next\_: `Callable[[], None]`

An alias of `next()` for avoiding the Python built-in method overrides in middleware functions

#### \_\_init\_\_

```python
def __init__(*,
             logger: logging.Logger,
             client: WebClient,
             req: BoltRequest,
             resp: BoltResponse,
             context: BoltContext,
             body: Dict[str, Any],
             payload: Dict[str, Any],
             options: Optional[Dict[str, Any]] = None,
             shortcut: Optional[Dict[str, Any]] = None,
             action: Optional[Dict[str, Any]] = None,
             view: Optional[Dict[str, Any]] = None,
             command: Optional[Dict[str, Any]] = None,
             event: Optional[Dict[str, Any]] = None,
             message: Optional[Dict[str, Any]] = None,
             ack: Ack,
             say: Say,
             respond: Respond,
             complete: Complete,
             fail: Fail,
             set_status: Optional[SetStatus] = None,
             set_title: Optional[SetTitle] = None,
             set_suggested_prompts: Optional[SetSuggestedPrompts] = None,
             get_thread_context: Optional[GetThreadContext] = None,
             save_thread_context: Optional[SaveThreadContext] = None,
             say_stream: Optional[SayStream] = None,
             next: Callable[[], None],
             **kwargs)
```

