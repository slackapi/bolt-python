---
sidebar_label: async_context
title: slack_bolt.context.async_context
---

## AsyncBoltContext Objects

```python
class AsyncBoltContext(BaseContext)
```

Context object associated with a request from Slack.

#### to\_copyable

```python
def to_copyable() -> AsyncBoltContext
```

#### listener\_runner

```python
@property
def listener_runner() -> AsyncioListenerRunner
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

- `AsyncWebClient` - `AsyncWebClient` instance

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

- `AsyncAck` - Callable `ack()` function

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

- `AsyncSay` - Callable `say()` function

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

- `Optional[AsyncRespond]` - Callable `respond()` function

#### complete

```python
@property
def complete() -> AsyncComplete
```

`complete()` function for this request. Once a custom function's state is set to complete,
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

- `AsyncComplete` - Callable `complete()` function

#### fail

```python
@property
def fail() -> AsyncFail
```

`fail()` function for this request. Once a custom function's state is set to error,
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

- `AsyncFail` - Callable `fail()` function

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
