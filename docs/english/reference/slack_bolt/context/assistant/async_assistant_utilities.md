---
sidebar_label: async_assistant_utilities
title: slack_bolt.context.assistant.async_assistant_utilities
---

## AsyncAssistantThreadContextStore Objects

```python
class AsyncAssistantThreadContextStore()
```

#### save

```python
async def save(*, channel_id: str, thread_ts: str, context: Dict[str,
                                                                 str]) -> None
```

#### find

```python
async def find(*, channel_id: str,
               thread_ts: str) -> Optional[AssistantThreadContext]
```

## DefaultAsyncAssistantThreadContextStore Objects

```python
class DefaultAsyncAssistantThreadContextStore(AsyncAssistantThreadContextStore
                                              )
```

#### client

#### context

#### save

```python
async def save(*, channel_id: str, thread_ts: str, context: Dict[str,
                                                                 str]) -> None
```

#### find

```python
async def find(*, channel_id: str,
               thread_ts: str) -> Optional[AssistantThreadContext]
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

## AsyncSay Objects

```python
class AsyncSay()
```

#### client

#### channel

#### thread\_ts

#### build\_metadata

#### has\_channel\_id\_and\_thread\_ts

```python
def has_channel_id_and_thread_ts(payload: dict) -> bool
```

Verifies if the given payload has both channel_id and thread_ts under assistant_thread property.
This data pattern is available for assistant_* events.

## AsyncGetThreadContext Objects

```python
class AsyncGetThreadContext()
```

#### thread\_context\_store

#### payload

#### channel\_id

#### thread\_ts

#### thread\_context\_loaded

## AsyncSaveThreadContext Objects

```python
class AsyncSaveThreadContext()
```

#### thread\_context\_store

#### channel\_id

#### thread\_ts

## AsyncSetTitle Objects

```python
class AsyncSetTitle()
```

#### client

#### channel\_id

#### thread\_ts

## AsyncAssistantUtilities Objects

```python
class AsyncAssistantUtilities()
```

#### payload

#### client

#### channel\_id

#### thread\_ts

#### thread\_context\_store

#### set\_title

```python
@property
def set_title() -> AsyncSetTitle
```

#### say

```python
@property
def say() -> AsyncSay
```

#### get\_thread\_context

```python
@property
def get_thread_context() -> AsyncGetThreadContext
```

#### save\_thread\_context

```python
@property
def save_thread_context() -> AsyncSaveThreadContext
```

