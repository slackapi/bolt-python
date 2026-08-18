---
sidebar_label: async_args
title: slack_bolt.kwargs_injection.async_args
---

## AsyncAck Objects

```python
class AsyncAck()
```

#### response

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

#### client

#### function\_execution\_id

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

#### client

#### function\_execution\_id

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

#### response\_url

#### proxy

#### ssl

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

#### thread\_context\_store

#### payload

#### channel\_id

#### thread\_ts

#### thread\_context\_loaded

#### \_\_init\_\_

```python
def __init__(thread_context_store: AsyncAssistantThreadContextStore,
             channel_id: str, thread_ts: str, payload: dict)
```

## AsyncSaveThreadContext Objects

```python
class AsyncSaveThreadContext()
```

#### thread\_context\_store

#### channel\_id

#### thread\_ts

#### \_\_init\_\_

```python
def __init__(thread_context_store: AsyncAssistantThreadContextStore,
             channel_id: str, thread_ts: str)
```

## AsyncSay Objects

```python
class AsyncSay()
```

#### client

#### channel

#### thread\_ts

#### build\_metadata

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

#### client

#### channel

#### recipient\_team\_id

#### recipient\_user\_id

#### thread\_ts

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

#### client

#### channel\_id

#### thread\_ts

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient, channel_id: str, thread_ts: str)
```

## AsyncSetSuggestedPrompts Objects

```python
class AsyncSetSuggestedPrompts()
```

#### client

#### channel\_id

#### thread\_ts

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

#### client

#### channel\_id

#### thread\_ts

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient, channel_id: str, thread_ts: str)
```

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body

#### body

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### query

The query string data in any data format.

#### headers

The request headers.

#### content\_type

#### context

The context in this request.

#### lazy\_only

#### lazy\_function\_name

#### mode

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

#### status

HTTP status code

#### body

The response body (dict and str are supported)

#### headers

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

#### logger

Logger instance

#### client

`slack_sdk.web.async_client.AsyncWebClient` instance with a valid token

#### req

Incoming request from Slack

#### resp

Response representation

#### request

Incoming request from Slack

#### response

Response representation

#### context

Context data associated with the incoming request

#### body

Parsed request body data

#### payload

The unwrapped core data in the request body

#### options

An alias for payload in an `@app.options` listener

#### shortcut

An alias for payload in an `@app.shortcut` listener

#### action

An alias for payload in an `@app.action` listener

#### view

An alias for payload in an `@app.view` listener

#### command

An alias for payload in an `@app.command` listener

#### event

An alias for payload in an `@app.event` listener

#### message

An alias for payload in an `@app.message` listener

#### ack

`ack()` utility function, which returns acknowledgement to the Slack servers

#### say

`say()` utility function, which calls chat.postMessage API with the associated channel ID

#### respond

`respond()` utility function, which utilizes the associated `response_url`

#### complete

`complete()` utility function, signals a successful completion of the custom function

#### fail

`fail()` utility function, signal that the custom function failed to complete

#### set\_status

`set_status()` utility function for AI Agents &amp; Assistants

#### set\_title

`set_title()` utility function for AI Agents &amp; Assistants

#### set\_suggested\_prompts

`set_suggested_prompts()` utility function for AI Agents &amp; Assistants

#### get\_thread\_context

`get_thread_context()` utility function for AI Agents &amp; Assistants

#### save\_thread\_context

`save_thread_context()` utility function for AI Agents &amp; Assistants

#### say\_stream

`say_stream()` utility function for AI Agents &amp; Assistants

#### next

`next()` utility function, which tells the middleware chain that it can continue with the next one

#### next\_

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

