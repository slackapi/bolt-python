---
sidebar_label: internals
title: slack_bolt.request.internals
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

#### parse\_query

```python
def parse_query(
    query: Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]]
) -> Dict[str, Sequence[str]]
```

#### parse\_body

```python
def parse_body(body: str, content_type: Optional[str]) -> Dict[str, Any]
```

#### extract\_is\_enterprise\_install

```python
def extract_is_enterprise_install(payload: Dict[str, Any]) -> Optional[bool]
```

#### extract\_enterprise\_id

```python
def extract_enterprise_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_actor\_enterprise\_id

```python
def extract_actor_enterprise_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_team\_id

```python
def extract_team_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_actor\_team\_id

```python
def extract_actor_team_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_user\_id

```python
def extract_user_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_actor\_user\_id

```python
def extract_actor_user_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_channel\_id

```python
def extract_channel_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_thread\_ts

```python
def extract_thread_ts(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_execution\_id

```python
def extract_function_execution_id(payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_bot\_access\_token

```python
def extract_function_bot_access_token(
        payload: Dict[str, Any]) -> Optional[str]
```

#### extract\_function\_inputs

```python
def extract_function_inputs(
        payload: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

#### build\_context

```python
def build_context(context: BoltContext, body: Dict[str, Any]) -> BoltContext
```

#### extract\_content\_type

```python
def extract_content_type(headers: Dict[str, Sequence[str]]) -> Optional[str]
```

#### build\_normalized\_headers

```python
def build_normalized_headers(
    headers: Optional[Dict[str, Union[str, Sequence[str]]]]
) -> Dict[str, Sequence[str]]
```

#### error\_message\_raw\_body\_required\_in\_http\_mode

```python
def error_message_raw_body_required_in_http_mode() -> str
```

#### debug\_multiple\_response\_urls\_detected

```python
def debug_multiple_response_urls_detected() -> str
```

