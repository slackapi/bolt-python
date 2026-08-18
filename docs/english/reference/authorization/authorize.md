---
sidebar_label: authorize
title: slack_bolt.authorization.authorize
---

## AuthorizeArgs Objects

```python
class AuthorizeArgs()
```

#### context

The request context

#### logger

#### client

#### enterprise\_id

The Organization ID (Enterprise Grid)

#### team\_id

The workspace ID

#### user\_id

The request user ID

#### \_\_init\_\_

```python
def __init__(*, context: BoltContext, enterprise_id: Optional[str],
             team_id: Optional[str], user_id: Optional[str])
```

The full list of the arguments passed to `authorize` function.

**Arguments**:

- `context` - The request context
- `enterprise_id` - The Organization ID (Enterprise Grid)
- `team_id` - The workspace ID
- `user_id` - The request user ID

## AuthorizeResult Objects

```python
class AuthorizeResult(dict)
```

Authorize function call result

#### enterprise\_id

Organization ID (Enterprise Grid) starting with `E`

#### team\_id

Workspace ID starting with `T`

#### team

Workspace name

#### url

Workspace slack.com URL

#### bot\_id

Bot ID starting with `B`

#### bot\_user\_id

Bot user&#x27;s User ID starting with either `U` or `W`

#### bot\_token

Bot user access token starting with `xoxb-`

#### bot\_scopes

The scopes associated with the bot token

#### user\_id

The request user ID

#### user

The request user&#x27;s name

#### user\_token

User access token starting with `xoxp-`

#### user\_scopes

The scopes associated wth the user token

#### \_\_init\_\_

```python
def __init__(*,
             enterprise_id: Optional[str],
             team_id: Optional[str],
             team: Optional[str] = None,
             url: Optional[str] = None,
             bot_user_id: Optional[str] = None,
             bot_id: Optional[str] = None,
             bot_token: Optional[str] = None,
             bot_scopes: Optional[Union[Sequence[str], str]] = None,
             user_id: Optional[str] = None,
             user: Optional[str] = None,
             user_token: Optional[str] = None,
             user_scopes: Optional[Union[Sequence[str], str]] = None)
```

**Arguments**:

- `enterprise_id` - Organization ID (Enterprise Grid) starting with `E`
- `team_id` - Workspace ID starting with `T`
- `team` - Workspace name
- `url` - Workspace slack.com URL
- `bot_user_id` - Bot user&#x27;s User ID starting with either `U` or `W`
- `bot_id` - Bot ID starting with `B`
- `bot_token` - Bot user access token starting with `xoxb-`
- `bot_scopes` - The scopes associated with the bot token
- `user_id` - The request user ID
- `user` - The request user&#x27;s name
- `user_token` - User access token starting with `xoxp-`
- `user_scopes` - The scopes associated wth the user token

#### from\_auth\_test\_response

```python
@classmethod
def from_auth_test_response(
    cls,
    *,
    bot_token: Optional[str] = None,
    user_token: Optional[str] = None,
    bot_scopes: Optional[Union[Sequence[str], str]] = None,
    user_scopes: Optional[Union[Sequence[str], str]] = None,
    auth_test_response: Union[SlackResponse, "AsyncSlackResponse"],
    user_auth_test_response: Optional[Union[SlackResponse,
                                            "AsyncSlackResponse"]] = None
) -> "AuthorizeResult"
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

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
```

## Authorize Objects

```python
class Authorize()
```

This provides authorize function that returns AuthorizeResult
for an incoming request from Slack.

#### \_\_init\_\_

```python
def __init__()
```

## CallableAuthorize Objects

```python
class CallableAuthorize(Authorize)
```

When you pass the `authorize` argument in AsyncApp constructor,
This `authorize` implementation will be used.

#### \_\_init\_\_

```python
def __init__(*, logger: Logger, func: Callable[..., AuthorizeResult])
```

## InstallationStoreAuthorize Objects

```python
class InstallationStoreAuthorize(Authorize)
```

If you use the OAuth flow settings, this `authorize` implementation will be used.
As long as your own InstallationStore (or the built-in ones) works as you expect,
you can expect that the `authorize` layer should work for you without any customization.

#### authorize\_result\_cache

#### bot\_only

#### user\_token\_resolution

#### find\_installation\_available

#### find\_bot\_available

#### token\_rotator

#### \_\_init\_\_

```python
def __init__(*,
             logger: Logger,
             installation_store: InstallationStore,
             client_id: Optional[str] = None,
             client_secret: Optional[str] = None,
             token_rotation_expiration_minutes: Optional[int] = None,
             bot_only: bool = False,
             cache_enabled: bool = False,
             client: Optional[WebClient] = None,
             user_token_resolution: str = "authed_user")
```

