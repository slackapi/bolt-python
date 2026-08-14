---
sidebar_label: async_handler
title: slack_bolt.adapter.sanic.async_handler
---

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

#### \_\_init\_\_

```python
def __init__(*,
             status: int,
             body: Union[str, dict] = "",
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None)
```

The response from a Bolt app.

**Arguments**:

- `status` - HTTP status code
- `body` - The response body (dict and str are supported)
- `headers` - The response headers.

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

## AsyncApp Objects

```python
class AsyncApp()
```

#### \_\_init\_\_

```python
def __init__(
        *,
        logger: Optional[logging.Logger] = None,
        name: Optional[str] = None,
        process_before_response: bool = False,
        raise_error_for_unhandled_request: bool = False,
        signing_secret: Optional[str] = None,
        token: Optional[str] = None,
        client: Optional[AsyncWebClient] = None,
        before_authorize: Optional[Union[AsyncMiddleware,
                                         Callable[...,
                                                  Awaitable[Any]]]] = None,
        authorize: Optional[Callable[..., Awaitable[AuthorizeResult]]] = None,
        user_facing_authorize_error_message: Optional[str] = None,
        installation_store: Optional[AsyncInstallationStore] = None,
        installation_store_bot_only: Optional[bool] = None,
        request_verification_enabled: bool = True,
        ignoring_self_events_enabled: bool = True,
        ignoring_self_assistant_message_events_enabled: bool = True,
        ssl_check_enabled: bool = True,
        url_verification_enabled: bool = True,
        attaching_function_token_enabled: bool = True,
        oauth_settings: Optional[AsyncOAuthSettings] = None,
        oauth_flow: Optional[AsyncOAuthFlow] = None,
        verification_token: Optional[str] = None,
        assistant_thread_context_store: Optional[
            AsyncAssistantThreadContextStore] = None,
        attaching_conversation_kwargs_enabled: bool = True)
```

Bolt App that provides functionalities to register middleware/listeners.

```python
    import os
    from slack_bolt.async_app import AsyncApp

    # Initializes your app with your bot token and signing secret
    app = AsyncApp(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
    )

    # Listens to incoming messages that contain "hello"
    @app.message("hello")
    async def message_hello(message, say):  # async function
        # say() sends a message to the channel where the event was triggered
        await say(f"Hey there <@{message['user']}>!")

    # Start your app
    if __name__ == "__main__":
        app.start(port=int(os.environ.get("PORT", 3000)))
```

Refer to https://docs.slack.dev/tools/bolt-python/concepts/async for details.

If you would like to build an OAuth app for enabling the app to run with multiple workspaces,
refer to https://docs.slack.dev/tools/bolt-python/concepts/authenticating-oauth to learn how to configure the app.

**Arguments**:

- `logger` - The custom logger that can be used in this app.
- `name` - The application name that will be used in logging. If absent, the source file name will be used.
- `process_before_response` - True if this app runs on Function as a Service. (Default: False)
- `raise_error_for_unhandled_request` - True if you want to raise exceptions for unhandled requests
  and use @app.error listeners instead of
  the built-in handler, which pints warning logs and returns 404 to Slack (Default: False)
- `signing_secret` - The Signing Secret value used for verifying requests from Slack.
- `token` - The bot/user access token required only for single-workspace app.
- `client` - The singleton `slack_sdk.web.async_client.AsyncWebClient` instance for this app.
- `before_authorize` - A global middleware that can be executed right before authorize function
- `authorize` - The function to authorize an incoming request from Slack
  by checking if there is a team/user in the installation data.
- `user_facing_authorize_error_message` - The user-facing error message to display
  when the app is installed but the installation is not managed by this app&#x27;s installation store
- `installation_store` - The module offering save/find operations of installation data
- `installation_store_bot_only` - Use `AsyncInstallationStore#async_find_bot()` if True (Default: False)
- `request_verification_enabled` - False if you would like to disable the built-in middleware (Default: True).
  `AsyncRequestVerification` is a built-in middleware that verifies the signature in HTTP Mode requests.
  Make sure if it&#x27;s safe enough when you turn a built-in middleware off.
  We strongly recommend using RequestVerification for better security.
  If you have a proxy that verifies request signature in front of the Bolt app,
  it&#x27;s totally fine to disable RequestVerification to avoid duplication of work.
  Don&#x27;t turn it off just for easiness of development.
- `ignoring_self_events_enabled` - False if you would like to disable the built-in middleware (Default: True).
  `AsyncIgnoringSelfEvents` is a built-in middleware that enables Bolt apps to easily skip the events
  generated by this app&#x27;s bot user (this is useful for avoiding code error causing an infinite loop).
- `ignoring_self_assistant_message_events_enabled` - False if you would like to disable the built-in middleware.
  `IgnoringSelfEvents` for this app&#x27;s bot user message events within an assistant thread
  This is useful for avoiding code error causing an infinite loop; Default: True
- `url_verification_enabled` - False if you would like to disable the built-in middleware (Default: True).
  `AsyncUrlVerification` is a built-in middleware that handles url_verification requests
  that verify the endpoint for Events API in HTTP Mode requests.
- `ssl_check_enabled` - bool = False if you would like to disable the built-in middleware (Default: True).
  `AsyncSslCheck` is a built-in middleware that handles ssl_check requests from Slack.
- `attaching_function_token_enabled` - False if you would like to disable the built-in middleware (Default: True).
  `AsyncAttachingFunctionToken` is a built-in middleware that injects the just-in-time workflow-execution token
  when your app receives `function_executed` or interactivity events scoped to a custom step.
- `oauth_settings` - The settings related to Slack app installation flow (OAuth flow)
- `oauth_flow` - Instantiated `slack_bolt.oauth.AsyncOAuthFlow`. This is always prioritized over oauth_settings.
- `verification_token` - Deprecated verification mechanism. This can be used only for ssl_check requests.
- `assistant_thread_context_store` - Custom AssistantThreadContext store (Default: the built-in implementation,
  which uses a parent message&#x27;s metadata to store the latest context)

#### name

```python
@property
def name() -> str
```

The name of this app (default: the filename)

#### oauth\_flow

```python
@property
def oauth_flow() -> Optional[AsyncOAuthFlow]
```

Configured `OAuthFlow` object if exists.

#### client

```python
@property
def client() -> AsyncWebClient
```

The singleton `slack_sdk.web.async_client.AsyncWebClient` instance in this app.

#### logger

```python
@property
def logger() -> logging.Logger
```

The logger this app uses.

#### installation\_store

```python
@property
def installation_store() -> Optional[AsyncInstallationStore]
```

The `slack_sdk.oauth.AsyncInstallationStore` that can be used in the `authorize` middleware.

#### listener\_runner

```python
@property
def listener_runner() -> AsyncioListenerRunner
```

The asyncio-based executor for asynchronously running listeners.

#### process\_before\_response

```python
@property
def process_before_response() -> bool
```

#### server

```python
def server(port: int = 3000,
           path: str = "/slack/events",
           host: Optional[str] = None) -> AsyncSlackAppServer
```

Configure a web server using AIOHTTP.
Refer to https://docs.aiohttp.org/ for more details about AIOHTTP.

**Arguments**:

- `port` - The port to listen on (Default: 3000)
- `path` - The path to handle request from Slack (Default: `/slack/events`)
- `host` - The hostname to serve the web endpoints. (Default: 0.0.0.0)

#### web\_app

```python
def web_app(path: str = "/slack/events", port: int = 3000) -> web.Application
```

Returns a `web.Application` instance for aiohttp-devtools users.

```python
    from slack_bolt.async_app import AsyncApp
    app = AsyncApp()

    @app.event("app_mention")
    async def event_test(body, say, logger):
        logger.info(body)
        await say("What's up?")

    def app_factory():
        return app.web_app()

    # adev runserver --port 3000 --app-factory app_factory async_app.py
```

**Arguments**:

- `path` - The path to receive incoming requests from Slack
- `port` - The port to listen on (Default: 3000)

#### start

```python
def start(port: int = 3000,
          path: str = "/slack/events",
          host: Optional[str] = None) -> None
```

Start a web server using AIOHTTP.
Refer to https://docs.aiohttp.org/ for more details about AIOHTTP.

**Arguments**:

- `port` - The port to listen on (Default: 3000)
- `path` - The path to handle request from Slack (Default: `/slack/events`)
- `host` - The hostname to serve the web endpoints. (Default: 0.0.0.0)

#### async\_dispatch

```python
async def async_dispatch(req: AsyncBoltRequest) -> BoltResponse
```

Applies all middleware and dispatches an incoming request from Slack to the right code path.

**Arguments**:

- `req` - An incoming request from Slack.
  

**Returns**:

  The response generated by this Bolt app.

#### use

```python
def use(*args) -> Optional[Callable]
```

Refer to `AsyncApp#middleware()` method&#x27;s docstring for details.

#### middleware

```python
def middleware(*args) -> Optional[Callable]
```

Registers a new middleware to this app.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.middleware
    async def middleware_func(logger, body, next):
        logger.info(f"request body: {body}")
        await next()
```

```python
    # Pass a function to this method
    app.middleware(middleware_func)
```

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `*args` - A function that works as a global middleware.

#### assistant

```python
def assistant(assistant: AsyncAssistant) -> Optional[Callable]
```

#### step

```python
def step(callback_id: Union[str, Pattern, AsyncWorkflowStep,
                            AsyncWorkflowStepBuilder],
         edit: Optional[Union[Callable[..., Optional[BoltResponse]],
                              AsyncListener, Sequence[Callable]]] = None,
         save: Optional[Union[Callable[..., Optional[BoltResponse]],
                              AsyncListener, Sequence[Callable]]] = None,
         execute: Optional[Union[Callable[..., Optional[BoltResponse]],
                                 AsyncListener, Sequence[Callable]]] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new step from app listener.

Unlike others, this method doesn&#x27;t behave as a decorator.
If you want to register a step from app by a decorator, use `AsyncWorkflowStepBuilder`&#x27;s methods.

```python
    # Create a new WorkflowStep instance
    from slack_bolt.workflows.async_step import AsyncWorkflowStep
    ws = AsyncWorkflowStep(
        callback_id="add_task",
        edit=edit,
        save=save,
        execute=execute,
    )
    # Pass Step to set up listeners
    app.step(ws)
```

Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details of steps from apps.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.
For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `callback_id` - The Callback ID for this step from app
- `edit` - The function for displaying a modal in the Workflow Builder
- `save` - The function for handling configuration in the Workflow Builder
- `execute` - The function for handling the step execution

#### error

```python
def error(
    func: Callable[..., Awaitable[Optional[BoltResponse]]]
) -> Callable[..., Awaitable[Optional[BoltResponse]]]
```

Updates the global error handler. This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.error
    async def custom_error_handler(error, body, logger):
        logger.exception(f"Error: {error}")
        logger.info(f"Request body: {body}")
```

```python
    # Pass a function to this method
    app.error(custom_error_handler)
```

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `func` - The function that is supposed to be executed
  when getting an unhandled error in Bolt app.

#### event

```python
def event(
    event: Union[
        str,
        Pattern,
        Dict[str, Optional[Union[str, Sequence[Optional[Union[str,
                                                              Pattern]]]]]],
    ],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new event listener. This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.event("team_join")
    async def ask_for_introduction(event, say):
        welcome_channel_id = "C12345"
        user_id = event["user"]
        text = f"Welcome to the team, <@{user_id}>! :tada: You can introduce yourself in this channel."
        await say(text=text, channel=welcome_channel_id)
```

```python
    # Pass a function to this method
    app.event("team_join")(ask_for_introduction)
```

Refer to https://docs.slack.dev/apis/events-api/ for details of Events API.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `event` - The conditions that match a request payload.
  If you pass a dict for this, you can have type, subtype in the constraint.
- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### message

```python
def message(
    keyword: Union[str, Pattern] = "",
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new message event listener. This method can be used as either a decorator or a method.
Check the `App#event` method&#x27;s docstring for details.

```python
    # Use this method as a decorator
    @app.message(":wave:")
    async def say_hello(message, say):
        user = message['user']
        await say(f"Hi there, <@{user}>!")
```

```python
    # Pass a function to this method
    app.message(":wave:")(say_hello)
```

Refer to https://docs.slack.dev/reference/events/message/ for details of `message` events.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `keyword` - The keyword to match
- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### function

```python
def function(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None,
    auto_acknowledge: bool = True,
    ack_timeout: int = 3
) -> Callable[..., Optional[Callable[..., Awaitable[BoltResponse]]]]
```

Registers a new Function listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.function("reverse")
    async def reverse_string(ack: AsyncAck, inputs: dict, complete: AsyncComplete, fail: AsyncFail):
        try:
            await ack()
            string_to_reverse = inputs["stringToReverse"]
            await complete({"reverseString": string_to_reverse[::-1]})
        except Exception as e:
            await fail(f"Cannot reverse string (error: {e})")
            raise e
```

```python
    # Pass a function to this method
    app.function("reverse")(reverse_string)
```

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `callback_id` - The callback id to identify the function
- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### command

```python
def command(
    command: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new slash command listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.command("/echo")
    async def repeat_text(ack, say, command):
        # Acknowledge command request
        await ack()
        await say(f"{command['text']}")
```

```python
    # Pass a function to this method
    app.command("/echo")(repeat_text)
```

Refer to https://docs.slack.dev/interactivity/implementing-slash-commands/ for details of Slash Commands.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `command` - The conditions that match a request payload
- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### shortcut

```python
def shortcut(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new shortcut listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.shortcut("open_modal")
    async def open_modal(ack, body, client):
        # Acknowledge the command request
        await ack()
        # Call views_open with the built-in client
        await client.views_open(
            # Pass a valid trigger_id within 3 seconds of receiving it
            trigger_id=body["trigger_id"],
            # View payload
            view={ ... }
        )
```

```python
    # Pass a function to this method
    app.shortcut("open_modal")(open_modal)
```

Refer to https://docs.slack.dev/interactivity/implementing-shortcuts/ for details about Shortcuts.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `constraints` - The conditions that match a request payload.
- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### global\_shortcut

```python
def global_shortcut(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new global shortcut listener.

#### message\_shortcut

```python
def message_shortcut(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new message shortcut listener.

#### action

```python
def action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new action listener. This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.action("approve_button")
    async def update_message(ack):
        await ack()
```

```python
    # Pass a function to this method
    app.action("approve_button")(update_message)
```

* Refer to https://docs.slack.dev/reference/interaction-payloads/block_actions-payload/ for actions in `blocks`.
* Refer to https://docs.slack.dev/legacy/legacy-messaging/legacy-message-buttons/ for actions in `attachments`.
* Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for actions in dialogs.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `constraints` - The conditions that match a request payload
- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### block\_action

```python
def block_action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `block_actions` action listener.
Refer to https://docs.slack.dev/reference/interaction-payloads/block_actions-payload/ for details.

#### attachment\_action

```python
def attachment_action(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `interactive_message` action listener.
Refer to https://docs.slack.dev/legacy/legacy-messaging/legacy-message-buttons/ for details.

#### dialog\_submission

```python
def dialog_submission(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `dialog_submission` listener.
Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

#### dialog\_cancellation

```python
def dialog_cancellation(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `dialog_submission` listener.
Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

#### view

```python
def view(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `view_submission`/`view_closed` event listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.view("view_1")
    async def handle_submission(ack, body, client, view):
        # Assume there's an input block with `block_c` as the block_id and `dreamy_input`
        hopes_and_dreams = view["state"]["values"]["block_c"]["dreamy_input"]
        user = body["user"]["id"]
        # Validate the inputs
        errors = {}
        if hopes_and_dreams is not None and len(hopes_and_dreams) <= 5:
            errors["block_c"] = "The value must be longer than 5 characters"
        if len(errors) > 0:
            await ack(response_action="errors", errors=errors)
            return
        # Acknowledge the view_submission event and close the modal
        await ack()
        # Do whatever you want with the input data - here we're saving it to a DB
```

```python
    # Pass a function to this method
    app.view("view_1")(handle_submission)
```

Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload for details of payloads.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `constraints` - The conditions that match a request payload
- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### view\_submission

```python
def view_submission(
    constraints: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `view_submission` listener.
Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/`view_submission` for
details.

#### view\_closed

```python
def view_closed(
    constraints: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `view_closed` listener.
Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/`view_closed` for details.

#### options

```python
def options(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new options listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.options("menu_selection")
    async def show_menu_options(ack):
        options = [
            {
                "text": {"type": "plain_text", "text": "Option 1"},
                "value": "1-1",
            },
            {
                "text": {"type": "plain_text", "text": "Option 2"},
                "value": "1-2",
            },
        ]
        await ack(options=options)
```

```python
    # Pass a function to this method
    app.options("menu_selection")(show_menu_options)
```

Refer to the following documents for details:

* https://docs.slack.dev/reference/block-kit/block-elements/select-menu-element#external_select
* https://docs.slack.dev/reference/block-kit/block-elements/multi-select-menu-element#external_multi_select

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`&#x27;s API document.

**Arguments**:

- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### block\_suggestion

```python
def block_suggestion(
    action_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `block_suggestion` listener.

#### dialog\_suggestion

```python
def dialog_suggestion(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., Awaitable[bool]]]] = None,
    middleware: Optional[Sequence[Union[Callable, AsyncMiddleware]]] = None
) -> Callable[..., Optional[Callable[..., Awaitable[Optional[BoltResponse]]]]]
```

Registers a new `dialog_suggestion` listener.
Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

#### default\_tokens\_revoked\_event\_listener

```python
def default_tokens_revoked_event_listener(
) -> Callable[..., Awaitable[Optional[BoltResponse]]]
```

#### default\_app\_uninstalled\_event\_listener

```python
def default_app_uninstalled_event_listener(
) -> Callable[..., Awaitable[Optional[BoltResponse]]]
```

#### enable\_token\_revocation\_listeners

```python
def enable_token_revocation_listeners() -> None
```

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body

#### body

#### query

#### headers

#### content\_type

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### \_\_init\_\_

```python
def __init__(*,
             body: Union[str, dict],
             query: Optional[Union[str, Dict[str, str],
                                   Dict[str, Sequence[str]]]] = None,
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
             context: Optional[Dict[str, Any]] = None,
             mode: str = "http")
```

Request to a Bolt app.

**Arguments**:

- `body` - The raw request body (only plain text is supported for &quot;http&quot; mode)
- `query` - The query string data in any data format.
- `headers` - The request headers.
- `context` - The context in this request.
- `mode` - The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

#### to\_copyable

```python
def to_copyable() -> "AsyncBoltRequest"
```

## AsyncOAuthFlow Objects

```python
class AsyncOAuthFlow()
```

#### settings

#### client\_id

#### redirect\_uri

#### install\_path

#### redirect\_uri\_path

#### success\_handler

#### failure\_handler

#### \_\_init\_\_

```python
def __init__(*,
             client: Optional[AsyncWebClient] = None,
             logger: Optional[Logger] = None,
             settings: AsyncOAuthSettings)
```

The module to run the Slack app installation flow (OAuth flow).

**Arguments**:

- `client` - The `slack_sdk.web.async_client.AsyncWebClient` instance.
- `logger` - The logger.
- `settings` - OAuth settings to configure this module.

#### client

```python
@property
def client() -> AsyncWebClient
```

#### logger

```python
@property
def logger() -> Logger
```

#### sqlite3

```python
@classmethod
def sqlite3(cls,
            database: str,
            authorization_url: Optional[str] = None,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            user_scopes: Optional[Sequence[str]] = None,
            redirect_uri: Optional[str] = None,
            install_path: Optional[str] = None,
            redirect_uri_path: Optional[str] = None,
            callback_options: Optional[AsyncCallbackOptions] = None,
            success_url: Optional[str] = None,
            failure_url: Optional[str] = None,
            state_cookie_name: str = OAuthStateUtils.default_cookie_name,
            state_expiration_seconds: int = OAuthStateUtils.
            default_expiration_seconds,
            installation_store_bot_only: bool = False,
            client: Optional[AsyncWebClient] = None,
            logger: Optional[Logger] = None) -> "AsyncOAuthFlow"
```

#### handle\_installation

```python
async def handle_installation(request: AsyncBoltRequest) -> BoltResponse
```

#### issue\_new\_state

```python
async def issue_new_state(request: AsyncBoltRequest) -> str
```

#### build\_authorize\_url

```python
async def build_authorize_url(state: str, request: AsyncBoltRequest) -> str
```

#### build\_install\_page\_html

```python
async def build_install_page_html(url: str, request: AsyncBoltRequest) -> str
```

#### append\_set\_cookie\_headers

```python
async def append_set_cookie_headers(headers: dict,
                                    set_cookie_value: Optional[str])
```

#### handle\_callback

```python
async def handle_callback(request: AsyncBoltRequest) -> BoltResponse
```

#### run\_installation

```python
async def run_installation(code: str) -> Optional[Installation]
```

#### store\_installation

```python
async def store_installation(request: AsyncBoltRequest,
                             installation: Installation)
```

#### to\_async\_bolt\_request

```python
def to_async_bolt_request(
    req: Request,
    addition_context_properties: Optional[Dict[str, Any]] = None
) -> AsyncBoltRequest
```

#### to\_sanic\_response

```python
def to_sanic_response(bolt_resp: BoltResponse) -> HTTPResponse
```

## AsyncSlackRequestHandler Objects

```python
class AsyncSlackRequestHandler()
```

#### \_\_init\_\_

```python
def __init__(app: AsyncApp)
```

#### handle

```python
async def handle(
    req: Request,
    addition_context_properties: Optional[Dict[str,
                                               Any]] = None) -> HTTPResponse
```

