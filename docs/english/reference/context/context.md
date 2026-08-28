---
sidebar_label: context
title: slack_bolt.context.context
slug: context
---

## BoltContext Objects

```python
class BoltContext(BaseContext)
```

Context object associated with a request from Slack.

#### to\_copyable

```python
def to_copyable() -> BoltContext
```

#### listener\_runner

```python
@property
def listener_runner() -> ThreadListenerRunner
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

- `WebClient` - `WebClient` instance

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

- `Ack` - Callable `ack()` function

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

- `Say` - Callable `say()` function

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

- `Optional[Respond]` - Callable `respond()` function

#### complete

```python
@property
def complete() -> Complete
```

`complete()` function for this request.

Once a custom function's state is set to complete,
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

- `Complete` - Callable `complete()` function

#### fail

```python
@property
def fail() -> Fail
```

`fail()` function for this request.

Once a custom function's state is set to error,
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

- `Fail` - Callable `fail()` function

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
