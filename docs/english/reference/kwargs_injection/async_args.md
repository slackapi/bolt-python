---
sidebar_label: async_args
title: slack_bolt.kwargs_injection.async_args
---

## AsyncAck Objects

```python
class AsyncAck()
```

#### response: `Optional[BoltResponse]`

#### \_\_init\_\_

```python
def __init__()
```

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

## AsyncComplete Objects

```python
class AsyncComplete()
```

#### client: `AsyncWebClient`

#### function\_execution\_id: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient, function_execution_id: Optional[str])
```

#### has\_been\_called

```python
def has_been_called() -> bool
```

Check if this complete function has been called.

**Returns**:

- `bool` - True if the complete function has been called, False otherwise.

## AsyncFail Objects

```python
class AsyncFail()
```

#### client: `AsyncWebClient`

#### function\_execution\_id: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient, function_execution_id: Optional[str])
```

#### has\_been\_called

```python
def has_been_called() -> bool
```

Check if this fail function has been called.

**Returns**:

- `bool` - True if the fail function has been called, False otherwise.

## AsyncRespond Objects

```python
class AsyncRespond()
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

## AsyncGetThreadContext Objects

```python
class AsyncGetThreadContext()
```

#### thread\_context\_store: `AsyncAssistantThreadContextStore`

#### payload: `dict`

#### channel\_id: `str`

#### thread\_ts: `str`

#### thread\_context\_loaded: `bool`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AsyncAssistantThreadContextStore,
             channel_id: str, thread_ts: str, payload: dict)
```

## AsyncSaveThreadContext Objects

```python
class AsyncSaveThreadContext()
```

#### thread\_context\_store: `AsyncAssistantThreadContextStore`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AsyncAssistantThreadContextStore,
             channel_id: str, thread_ts: str)
```

## AsyncSay Objects

```python
class AsyncSay()
```

#### client: `Optional[AsyncWebClient]`

#### channel: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### build\_metadata: `Optional[Callable[[], Awaitable[Union[Dict, Metadata]]]]`

#### \_\_init\_\_

```python
def __init__(
    client: Optional[AsyncWebClient],
    channel: Optional[str],
    thread_ts: Optional[str] = None,
    build_metadata: Optional[Callable[[], Awaitable[Union[Dict,
                                                          Metadata]]]] = None)
```

## AsyncSayStream Objects

```python
class AsyncSayStream()
```

#### client: `AsyncWebClient`

#### channel: `Optional[str]`

#### recipient\_team\_id: `Optional[str]`

#### recipient\_user\_id: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(*,
             client: AsyncWebClient,
             channel: Optional[str] = None,
             recipient_team_id: Optional[str] = None,
             recipient_user_id: Optional[str] = None,
             thread_ts: Optional[str] = None)
```

## AsyncSetStatus Objects

```python
class AsyncSetStatus()
```

#### client: `AsyncWebClient`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient, channel_id: str, thread_ts: str)
```

## AsyncSetSuggestedPrompts Objects

```python
class AsyncSetSuggestedPrompts()
```

#### client: `AsyncWebClient`

#### channel\_id: `str`

#### thread\_ts: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient,
             channel_id: str,
             thread_ts: Optional[str] = None)
```

## AsyncSetTitle Objects

```python
class AsyncSetTitle()
```

#### client: `AsyncWebClient`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient, channel_id: str, thread_ts: str)
```

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body: `str`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### context: `AsyncBoltContext`

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
def to_copyable() -> "AsyncBoltRequest"
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

## AsyncArgs Objects

```python
class AsyncArgs()
```

All the arguments in this class are available in any middleware / listeners.
You can inject the named variables in the argument list in arbitrary order.

```python
    @app.action("link_button")
    async def handle_buttons(ack, respond, logger, context, body, client):
        logger.info(f"request body: {body}")
        await ack()
        if context.channel_id is not None:
            await respond("Hi!")
        await client.views_open(
            trigger_id=body["trigger_id"],
            view={ ... }
        )
```

Alternatively, you can include a parameter named `args` and it will be injected with an instance of this class.

```python
    @app.action("link_button")
    async def handle_buttons(args):
        args.logger.info(f"request body: {args.body}")
        await args.ack()
        if args.context.channel_id is not None:
            await args.respond("Hi!")
        await args.client.views_open(
            trigger_id=args.body["trigger_id"],
            view={ ... }
        )
```

#### logger: `Logger`

Logger instance

#### client: `AsyncWebClient`

`slack_sdk.web.async_client.AsyncWebClient` instance with a valid token

#### req: `AsyncBoltRequest`

Incoming request from Slack

#### resp: `BoltResponse`

Response representation

#### request: `AsyncBoltRequest`

Incoming request from Slack

#### response: `BoltResponse`

Response representation

#### context: `AsyncBoltContext`

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

#### ack: `AsyncAck`

`ack()` utility function, which returns acknowledgement to the Slack servers

#### say: `AsyncSay`

`say()` utility function, which calls chat.postMessage API with the associated channel ID

#### respond: `AsyncRespond`

`respond()` utility function, which utilizes the associated `response_url`

#### complete: `AsyncComplete`

`complete()` utility function, signals a successful completion of the custom function

#### fail: `AsyncFail`

`fail()` utility function, signal that the custom function failed to complete

#### set\_status: `Optional[AsyncSetStatus]`

`set_status()` utility function for AI Agents &amp; Assistants

#### set\_title: `Optional[AsyncSetTitle]`

`set_title()` utility function for AI Agents &amp; Assistants

#### set\_suggested\_prompts: `Optional[AsyncSetSuggestedPrompts]`

`set_suggested_prompts()` utility function for AI Agents &amp; Assistants

#### get\_thread\_context: `Optional[AsyncGetThreadContext]`

`get_thread_context()` utility function for AI Agents &amp; Assistants

#### save\_thread\_context: `Optional[AsyncSaveThreadContext]`

`save_thread_context()` utility function for AI Agents &amp; Assistants

#### say\_stream: `Optional[AsyncSayStream]`

`say_stream()` utility function for AI Agents &amp; Assistants

#### next: `Callable[[], Awaitable[None]]`

`next()` utility function, which tells the middleware chain that it can continue with the next one

#### next\_: `Callable[[], Awaitable[None]]`

An alias of `next()` for avoiding the Python built-in method overrides in middleware functions

#### \_\_init\_\_

```python
def __init__(*,
             logger: Logger,
             client: AsyncWebClient,
             req: AsyncBoltRequest,
             resp: BoltResponse,
             context: AsyncBoltContext,
             body: Dict[str, Any],
             payload: Dict[str, Any],
             options: Optional[Dict[str, Any]] = None,
             shortcut: Optional[Dict[str, Any]] = None,
             action: Optional[Dict[str, Any]] = None,
             view: Optional[Dict[str, Any]] = None,
             command: Optional[Dict[str, Any]] = None,
             event: Optional[Dict[str, Any]] = None,
             message: Optional[Dict[str, Any]] = None,
             ack: AsyncAck,
             say: AsyncSay,
             respond: AsyncRespond,
             complete: AsyncComplete,
             fail: AsyncFail,
             set_status: Optional[AsyncSetStatus] = None,
             set_title: Optional[AsyncSetTitle] = None,
             set_suggested_prompts: Optional[AsyncSetSuggestedPrompts] = None,
             get_thread_context: Optional[AsyncGetThreadContext] = None,
             save_thread_context: Optional[AsyncSaveThreadContext] = None,
             say_stream: Optional[AsyncSayStream] = None,
             next: Callable[[], Awaitable[None]],
             **kwargs)
```

