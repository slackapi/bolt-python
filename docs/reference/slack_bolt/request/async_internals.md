---
sidebar_label: async_internals
title: slack_bolt.request.async_internals
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

#### extract\_enterprise\_id

```python
def extract_enterprise_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_bot\_access\_token

```python
def extract_function_bot_access_token(
        payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_execution\_id

```python
def extract_function_execution_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_inputs

```python
def extract_function_inputs(
        payload: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### extract\_is\_enterprise\_install

```python
def extract_is_enterprise_install(payload: Dict[str, Any]) -> Optional[bool]
```

#### extract\_team\_id

```python
def extract_team_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_user\_id

```python
def extract_user_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_channel\_id

```python
def extract_channel_id(payload: Dict[str, Any]) -> Optional[str]
```

#### debug\_multiple\_response\_urls\_detected

```python
def debug_multiple_response_urls_detected() -> str
```

#### extract\_actor\_enterprise\_id

```python
def extract_actor_enterprise_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_actor\_team\_id

```python
def extract_actor_team_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_actor\_user\_id

```python
def extract_actor_user_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_thread\_ts

```python
def extract_thread_ts(payload: Dict[str, Any]) -> Optional[str]
```

#### build\_async\_context

```python
def build_async_context(context: AsyncBoltContext,
                        body: Dict[str, Any]) -> AsyncBoltContext
```

