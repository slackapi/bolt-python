---
sidebar_label: async_args
title: slack_bolt.kwargs_injection.async_args
---

## `AsyncArgs`

```python
AsyncArgs(*, logger, client, req, resp, context, body, payload, options=None, shortcut=None, action=None, view=None, command=None, event=None, message=None, ack, say, respond, complete, fail, set_status=None, set_title=None, set_suggested_prompts=None, get_thread_context=None, save_thread_context=None, say_stream=None, next, **kwargs)
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

### `ack`

```python
ack: AsyncAck = ack
```

`ack()` utility function, which returns acknowledgement to the Slack servers

### `action`

```python
action: Optional[Dict[str, Any]] = action
```

An alias for payload in an `@app.action` listener

### `body`

```python
body: Dict[str, Any] = body
```

Parsed request body data

### `client`

```python
client: AsyncWebClient = client
```

`slack_sdk.web.async_client.AsyncWebClient` instance with a valid token

### `command`

```python
command: Optional[Dict[str, Any]] = command
```

An alias for payload in an `@app.command` listener

### `complete`

```python
complete: AsyncComplete = complete
```

`complete()` utility function, signals a successful completion of the custom function

### `context`

```python
context: AsyncBoltContext = context
```

Context data associated with the incoming request

### `event`

```python
event: Optional[Dict[str, Any]] = event
```

An alias for payload in an `@app.event` listener

### `fail`

```python
fail: AsyncFail = fail
```

`fail()` utility function, signal that the custom function failed to complete

### `get_thread_context`

```python
get_thread_context: Optional[AsyncGetThreadContext] = get_thread_context
```

`get_thread_context()` utility function for AI Agents & Assistants

### `logger`

```python
logger: Logger = logger
```

Logger instance

### `message`

```python
message: Optional[Dict[str, Any]] = message
```

An alias for payload in an `@app.message` listener

### `next`

```python
next: Callable[[], Awaitable[None]] = next
```

`next()` utility function, which tells the middleware chain that it can continue with the next one

### `next_`

```python
next_: Callable[[], Awaitable[None]] = next
```

An alias of `next()` for avoiding the Python built-in method overrides in middleware functions

### `options`

```python
options: Optional[Dict[str, Any]] = options
```

An alias for payload in an `@app.options` listener

### `payload`

```python
payload: Dict[str, Any] = payload
```

The unwrapped core data in the request body

### `req`

```python
req: AsyncBoltRequest = req
```

Incoming request from Slack

### `request`

```python
request: AsyncBoltRequest = req
```

Incoming request from Slack

### `resp`

```python
resp: BoltResponse = resp
```

Response representation

### `respond`

```python
respond: AsyncRespond = respond
```

`respond()` utility function, which utilizes the associated `response_url`

### `response`

```python
response: BoltResponse = resp
```

Response representation

### `save_thread_context`

```python
save_thread_context: Optional[AsyncSaveThreadContext] = save_thread_context
```

`save_thread_context()` utility function for AI Agents & Assistants

### `say`

```python
say: AsyncSay = say
```

`say()` utility function, which calls chat.postMessage API with the associated channel ID

### `say_stream`

```python
say_stream: Optional[AsyncSayStream] = say_stream
```

`say_stream()` utility function for AI Agents & Assistants

### `set_status`

```python
set_status: Optional[AsyncSetStatus] = set_status
```

`set_status()` utility function for AI Agents & Assistants

### `set_suggested_prompts`

```python
set_suggested_prompts: Optional[AsyncSetSuggestedPrompts] = set_suggested_prompts
```

`set_suggested_prompts()` utility function for AI Agents & Assistants

### `set_title`

```python
set_title: Optional[AsyncSetTitle] = set_title
```

`set_title()` utility function for AI Agents & Assistants

### `shortcut`

```python
shortcut: Optional[Dict[str, Any]] = shortcut
```

An alias for payload in an `@app.shortcut` listener

### `view`

```python
view: Optional[Dict[str, Any]] = view
```

An alias for payload in an `@app.view` listener
