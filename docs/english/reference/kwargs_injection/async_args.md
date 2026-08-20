---
sidebar_label: async_args
title: slack_bolt.kwargs_injection.async_args
---

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

`set_status()` utility function for AI Agents & Assistants

#### set\_title: `Optional[AsyncSetTitle]`

`set_title()` utility function for AI Agents & Assistants

#### set\_suggested\_prompts: `Optional[AsyncSetSuggestedPrompts]`

`set_suggested_prompts()` utility function for AI Agents & Assistants

#### get\_thread\_context: `Optional[AsyncGetThreadContext]`

`get_thread_context()` utility function for AI Agents & Assistants

#### save\_thread\_context: `Optional[AsyncSaveThreadContext]`

`save_thread_context()` utility function for AI Agents & Assistants

#### say\_stream: `Optional[AsyncSayStream]`

`say_stream()` utility function for AI Agents & Assistants

#### next: `Callable[[], Awaitable[None]]`

`next()` utility function, which tells the middleware chain that it can continue with the next one

#### next\_: `Callable[[], Awaitable[None]]`

An alias of `next()` for avoiding the Python built-in method overrides in middleware functions

#### \_\_init\_\_

```python
def __init__(
    *,
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
