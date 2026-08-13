---
sidebar_label: args
title: slack_bolt.kwargs_injection.args
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

## Ack Objects

```python
class Ack()
```

#### response

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

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body

#### query

#### headers

#### content\_type

#### body

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

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

## Args Objects

```python
class Args()
```

All the arguments in this class are available in any middleware / listeners.
You can inject the named variables in the argument list in arbitrary order.

```python
    @app.action("link_button")
    def handle_buttons(ack, respond, logger, context, body, client):
        logger.info(f"request body: {body}")
        ack()
        if context.channel_id is not None:
            respond("Hi!")
        client.views_open(
            trigger_id=body["trigger_id"],
            view={ ... }
        )
```

Alternatively, you can include a parameter named `args` and it will be injected with an instance of this class.

```python
    @app.action("link_button")
    def handle_buttons(args):
        args.logger.info(f"request body: {args.body}")
        args.ack()
        if args.context.channel_id is not None:
            args.respond("Hi!")
        args.client.views_open(
            trigger_id=args.body["trigger_id"],
            view={ ... }
        )
```

#### client

`slack_sdk.web.WebClient` instance with a valid token

#### logger

Logger instance

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

`say()` utility function, which calls `chat.postMessage` API with the associated channel ID

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

`say_stream()` utility function for conversations, AI Agents &amp; Assistants

#### next

`next()` utility function, which tells the middleware chain that it can continue with the next one

#### next\_

An alias of `next()` for avoiding the Python built-in method overrides in middleware functions

