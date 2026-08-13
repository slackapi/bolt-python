---
sidebar_label: context
title: slack_bolt.context.context
---

## Ack Objects

```python
class Ack()
```

#### response

## BaseContext Objects

```python
class BaseContext(dict)
```

Context object associated with a request from Slack.

#### copyable\_standard\_property\_names

#### non\_copyable\_standard\_property\_names

#### standard\_property\_names

#### logger

```python
@property
def logger() -> Logger
```

The properly configured logger that is available for middleware/listeners.

#### token

```python
@property
def token() -> Optional[str]
```

The (bot/user) token resolved for this request.

#### enterprise\_id

```python
@property
def enterprise_id() -> Optional[str]
```

The Enterprise Grid Organization ID of this request.

#### is\_enterprise\_install

```python
@property
def is_enterprise_install() -> Optional[bool]
```

True if the request is associated with an Org-wide installation.

#### team\_id

```python
@property
def team_id() -> Optional[str]
```

The Workspace ID of this request.

#### user\_id

```python
@property
def user_id() -> Optional[str]
```

The user ID associated ith this request.

#### actor\_enterprise\_id

```python
@property
def actor_enterprise_id() -> Optional[str]
```

The action&#x27;s actor&#x27;s Enterprise Grid organization ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it&#x27;s not guaranteed to have a valid ID for all events due to server-side inconsistency.

#### actor\_team\_id

```python
@property
def actor_team_id() -> Optional[str]
```

The action&#x27;s actor&#x27;s workspace ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it&#x27;s not guaranteed to have a valid ID for all events due to server-side inconsistency.

#### actor\_user\_id

```python
@property
def actor_user_id() -> Optional[str]
```

The action&#x27;s actor&#x27;s user ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it&#x27;s not guaranteed to have a valid ID for all events due to server-side inconsistency.

#### channel\_id

```python
@property
def channel_id() -> Optional[str]
```

The conversation ID associated with this request.

#### thread\_ts

```python
@property
def thread_ts() -> Optional[str]
```

The conversation thread&#x27;s ID associated with this request.

#### response\_url

```python
@property
def response_url() -> Optional[str]
```

The `response_url` associated with this request.

#### matches

```python
@property
def matches() -> Optional[Tuple]
```

Returns all the matched parts in message listener&#x27;s regexp

#### function\_execution\_id

```python
@property
def function_execution_id() -> Optional[str]
```

The `function_execution_id` associated with this request.
Only available for `function_executed` and interactivity events scoped to a custom step.

#### inputs

```python
@property
def inputs() -> Optional[Dict[str, Any]]
```

The `inputs` associated with this request.
Only available for `function_executed` and interactivity events scoped to a custom step.

#### authorize\_result

```python
@property
def authorize_result() -> Optional[AuthorizeResult]
```

The authorize result resolved for this request.

#### function\_bot\_access\_token

```python
@property
def function_bot_access_token() -> Optional[str]
```

The bot token resolved for this function request.
Only available for `function_executed` and interactivity events scoped to a custom step.

#### bot\_token

```python
@property
def bot_token() -> Optional[str]
```

The bot token resolved for this request.

#### bot\_id

```python
@property
def bot_id() -> Optional[str]
```

The bot ID resolved for this request.

#### bot\_user\_id

```python
@property
def bot_user_id() -> Optional[str]
```

The bot user ID resolved for this request.

#### user\_token

```python
@property
def user_token() -> Optional[str]
```

The user token resolved for this request.

#### set\_authorize\_result

```python
def set_authorize_result(authorize_result: AuthorizeResult)
```

## Complete Objects

```python
class Complete()
```

#### client

#### function\_execution\_id

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

#### client

#### function\_execution\_id

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

#### thread\_context\_store

#### payload

#### channel\_id

#### thread\_ts

#### thread\_context\_loaded

## Respond Objects

```python
class Respond()
```

#### response\_url

#### proxy

#### ssl

## SaveThreadContext Objects

```python
class SaveThreadContext()
```

#### thread\_context\_store

#### channel\_id

#### thread\_ts

## Say Objects

```python
class Say()
```

#### client

#### channel

#### thread\_ts

#### metadata

#### build\_metadata

## SayStream Objects

```python
class SayStream()
```

#### client

#### channel

#### recipient\_team\_id

#### recipient\_user\_id

#### thread\_ts

## SetStatus Objects

```python
class SetStatus()
```

#### client

#### channel\_id

#### thread\_ts

## SetSuggestedPrompts Objects

```python
class SetSuggestedPrompts()
```

#### client

#### channel\_id

#### thread\_ts

## SetTitle Objects

```python
class SetTitle()
```

#### client

#### channel\_id

#### thread\_ts

#### create\_copy

```python
def create_copy(original: Any) -> Any
```

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

