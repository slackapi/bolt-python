---
sidebar_label: websocket_client
title: slack_bolt.adapter.socket_mode.websocket_client
---

[`websocket-client`](https://pypi.org/project/websocket-client/) based implementation

## App Objects

```python
class App()
```

#### \_\_init\_\_

```python
def __init__(*,
             logger: Optional[logging.Logger] = None,
             name: Optional[str] = None,
             process_before_response: bool = False,
             raise_error_for_unhandled_request: bool = False,
             signing_secret: Optional[str] = None,
             token: Optional[str] = None,
             token_verification_enabled: bool = True,
             client: Optional[WebClient] = None,
             before_authorize: Optional[Union[Middleware,
                                              Callable[..., Any]]] = None,
             authorize: Optional[Callable[..., AuthorizeResult]] = None,
             user_facing_authorize_error_message: Optional[str] = None,
             installation_store: Optional[InstallationStore] = None,
             installation_store_bot_only: Optional[bool] = None,
             request_verification_enabled: bool = True,
             ignoring_self_events_enabled: bool = True,
             ignoring_self_assistant_message_events_enabled: bool = True,
             ssl_check_enabled: bool = True,
             url_verification_enabled: bool = True,
             attaching_function_token_enabled: bool = True,
             oauth_settings: Optional[OAuthSettings] = None,
             oauth_flow: Optional[OAuthFlow] = None,
             verification_token: Optional[str] = None,
             listener_executor: Optional[Executor] = None,
             assistant_thread_context_store: Optional[
                 AssistantThreadContextStore] = None,
             attaching_conversation_kwargs_enabled: bool = True)
```

Bolt App that provides functionalities to register middleware/listeners.

```python
    import os
    from slack_bolt import App

    # Initializes your app with your bot token and signing secret
    app = App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
    )

    # Listens to incoming messages that contain "hello"
    @app.message("hello")
    def message_hello(message, say):
        # say() sends a message to the channel where the event was triggered
        say(f"Hey there <@{message['user']}>!")

    # Start your app
    if __name__ == "__main__":
        app.start(port=int(os.environ.get("PORT", 3000)))
```

Refer to https://docs.slack.dev/tools/bolt-python/creating-an-app for details.

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
- `token_verification_enabled` - Verifies the validity of the given token if True.
- `client` - The singleton `slack_sdk.WebClient` instance for this app.
- `before_authorize` - A global middleware that can be executed right before authorize function
- `authorize` - The function to authorize an incoming request from Slack
  by checking if there is a team/user in the installation data.
- `user_facing_authorize_error_message` - The user-facing error message to display
  when the app is installed but the installation is not managed by this app&#x27;s installation store
- `installation_store` - The module offering save/find operations of installation data
- `installation_store_bot_only` - Use `InstallationStore#find_bot()` if True (Default: False)
- `request_verification_enabled` - False if you would like to disable the built-in middleware (Default: True).
  `RequestVerification` is a built-in middleware that verifies the signature in HTTP Mode requests.
  Make sure if it&#x27;s safe enough when you turn a built-in middleware off.
  We strongly recommend using RequestVerification for better security.
  If you have a proxy that verifies request signature in front of the Bolt app,
  it&#x27;s totally fine to disable RequestVerification to avoid duplication of work.
  Don&#x27;t turn it off just for easiness of development.
- `ignoring_self_events_enabled` - False if you would like to disable the built-in middleware (Default: True).
  `IgnoringSelfEvents` is a built-in middleware that enables Bolt apps to easily skip the events
  generated by this app&#x27;s bot user (this is useful for avoiding code error causing an infinite loop).
- `ignoring_self_assistant_message_events_enabled` - False if you would like to disable the built-in middleware.
  `IgnoringSelfEvents` for this app&#x27;s bot user message events within an assistant thread
  This is useful for avoiding code error causing an infinite loop; Default: True
- `url_verification_enabled` - False if you would like to disable the built-in middleware (Default: True).
  `UrlVerification` is a built-in middleware that handles url_verification requests
  that verify the endpoint for Events API in HTTP Mode requests.
- `attaching_function_token_enabled` - False if you would like to disable the built-in middleware (Default: True).
  `AttachingFunctionToken` is a built-in middleware that injects the just-in-time workflow-execution tokens
  when your app receives `function_executed` or interactivity events scoped to a custom step.
- `ssl_check_enabled` - bool = False if you would like to disable the built-in middleware (Default: True).
  `SslCheck` is a built-in middleware that handles ssl_check requests from Slack.
- `oauth_settings` - The settings related to Slack app installation flow (OAuth flow)
- `oauth_flow` - Instantiated `slack_bolt.oauth.OAuthFlow`. This is always prioritized over oauth_settings.
- `verification_token` - Deprecated verification mechanism. This can be used only for ssl_check requests.
- `listener_executor` - Custom executor to run background tasks. If absent, the default `ThreadPoolExecutor` will
  be used.
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
def oauth_flow() -> Optional[OAuthFlow]
```

Configured `OAuthFlow` object if exists.

#### logger

```python
@property
def logger() -> logging.Logger
```

The logger this app uses.

#### client

```python
@property
def client() -> WebClient
```

The singleton `slack_sdk.WebClient` instance in this app.

#### installation\_store

```python
@property
def installation_store() -> Optional[InstallationStore]
```

The `slack_sdk.oauth.InstallationStore` that can be used in the `authorize` middleware.

#### listener\_runner

```python
@property
def listener_runner() -> ThreadListenerRunner
```

The thread executor for asynchronously running listeners.

#### process\_before\_response

```python
@property
def process_before_response() -> bool
```

#### start

```python
def start(port: int = 3000,
          path: str = "/slack/events",
          http_server_logger_enabled: bool = True) -> None
```

Starts a web server for local development.

```python
    # With the default settings, `http://localhost:3000/slack/events`
    # is available for handling incoming requests from Slack
    app.start()
```

This method internally starts a Web server process built with the `http.server` module.
For production, consider using a production-ready WSGI server such as Gunicorn.

**Arguments**:

- `port` - The port to listen on (Default: 3000)
- `path` - The path to handle request from Slack (Default: `/slack/events`)
- `http_server_logger_enabled` - The flag to enable http.server logging if True (Default: True)

#### dispatch

```python
def dispatch(req: BoltRequest) -> BoltResponse
```

Applies all middleware and dispatches an incoming request from Slack to the right code path.

**Arguments**:

- `req` - An incoming request from Slack
  

**Returns**:

  The response generated by this Bolt app

#### use

```python
def use(*args) -> Optional[Callable]
```

Registers a new global middleware to this app. This method can be used as either a decorator or a method.

Refer to `App#middleware()` method&#x27;s docstring for details.

#### middleware

```python
def middleware(*args) -> Optional[Callable]
```

Registers a new middleware to this app.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.middleware
    def middleware_func(logger, body, next):
        logger.info(f"request body: {body}")
        next()
```

```python
    # Pass a function to this method
    app.middleware(middleware_func)
```

Refer to https://docs.slack.dev/tools/bolt-python/concepts/global-middleware for details.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

**Arguments**:

- `*args` - A function that works as a global middleware.

#### assistant

```python
def assistant(assistant: Assistant) -> Optional[Callable]
```

#### step

```python
def step(callback_id: Union[str, Pattern, WorkflowStep, WorkflowStepBuilder],
         edit: Optional[Union[Callable[..., Optional[BoltResponse]], Listener,
                              Sequence[Callable]]] = None,
         save: Optional[Union[Callable[..., Optional[BoltResponse]], Listener,
                              Sequence[Callable]]] = None,
         execute: Optional[Union[Callable[..., Optional[BoltResponse]],
                                 Listener, Sequence[Callable]]] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new step from app listener.

Unlike others, this method doesn&#x27;t behave as a decorator.
If you want to register a step from app by a decorator, use `WorkflowStepBuilder`&#x27;s methods.

```python
    # Create a new WorkflowStep instance
    from slack_bolt.workflows.step import WorkflowStep
    ws = WorkflowStep(
        callback_id="add_task",
        edit=edit,
        save=save,
        execute=execute,
    )
    # Pass Step to set up listeners
    app.step(ws)
```

Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details of steps from apps.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

For further information about WorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `callback_id` - The Callback ID for this step from app
- `edit` - The function for displaying a modal in the Workflow Builder
- `save` - The function for handling configuration in the Workflow Builder
- `execute` - The function for handling the step execution

#### error

```python
def error(
    func: Callable[..., Optional[BoltResponse]]
) -> Callable[..., Optional[BoltResponse]]
```

Updates the global error handler. This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.error
    def custom_error_handler(error, body, logger):
        logger.exception(f"Error: {error}")
        logger.info(f"Request body: {body}")
```

```python
    # Pass a function to this method
    app.error(custom_error_handler)
```

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

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
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new event listener. This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.event("team_join")
    def ask_for_introduction(event, say):
        welcome_channel_id = "C12345"
        user_id = event["user"]
        text = f"Welcome to the team, <@{user_id}>! :tada: You can introduce yourself in this channel."
        say(text=text, channel=welcome_channel_id)
```

```python
    # Pass a function to this method
    app.event("team_join")(ask_for_introduction)
```

Refer to https://docs.slack.dev/apis/events-api/ for details of Events API.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

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
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new message event listener. This method can be used as either a decorator or a method.
Check the `App#event` method&#x27;s docstring for details.

```python
    # Use this method as a decorator
    @app.message(":wave:")
    def say_hello(message, say):
        user = message['user']
        say(f"Hi there, <@{user}>!")
```

```python
    # Pass a function to this method
    app.message(":wave:")(say_hello)
```

Refer to https://docs.slack.dev/reference/events/message/ for details of `message` events.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

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
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None,
    auto_acknowledge: bool = True,
    ack_timeout: int = 3
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new Function listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.function("reverse")
    def reverse_string(ack: Ack, inputs: dict, complete: Complete, fail: Fail):
        try:
            ack()
            string_to_reverse = inputs["stringToReverse"]
            complete(outputs={"reverseString": string_to_reverse[::-1]})
        except Exception as e:
            fail(f"Cannot reverse string (error: {e})")
            raise e
```

```python
    # Pass a function to this method
    app.function("reverse")(reverse_string)
```

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

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
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new slash command listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.command("/echo")
    def repeat_text(ack, say, command):
        # Acknowledge command request
        ack()
        say(f"{command['text']}")
```

```python
    # Pass a function to this method
    app.command("/echo")(repeat_text)
```

Refer to https://docs.slack.dev/interactivity/implementing-slash-commands/ for details of Slash Commands.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

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
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new shortcut listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.shortcut("open_modal")
    def open_modal(ack, body, client):
        # Acknowledge the command request
        ack()
        # Call views_open with the built-in client
        client.views_open(
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

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

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
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new global shortcut listener.

#### message\_shortcut

```python
def message_shortcut(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new message shortcut listener.

#### action

```python
def action(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new action listener. This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.action("approve_button")
    def update_message(ack):
        ack()
```

```python
    # Pass a function to this method
    app.action("approve_button")(update_message)
```

* Refer to https://docs.slack.dev/reference/interaction-payloads/block_actions-payload/ for actions in `blocks`.
* Refer to https://docs.slack.dev/legacy/legacy-messaging/legacy-message-buttons/ for actions in `attachments`.
* Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for actions in dialogs.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

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
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `block_actions` action listener.
Refer to https://docs.slack.dev/reference/interaction-payloads/block_actions-payload/ for details.

#### attachment\_action

```python
def attachment_action(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `interactive_message` action listener.
Refer to https://docs.slack.dev/legacy/legacy-messaging/legacy-message-buttons/ for details.

#### dialog\_submission

```python
def dialog_submission(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `dialog_submission` listener.
Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

#### dialog\_cancellation

```python
def dialog_cancellation(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `dialog_cancellation` listener.
Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

#### view

```python
def view(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `view_submission`/`view_closed` event listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.view("view_1")
    def handle_submission(ack, body, client, view):
        # Assume there's an input block with `block_c` as the block_id and `dreamy_input`
        hopes_and_dreams = view["state"]["values"]["block_c"]["dreamy_input"]
        user = body["user"]["id"]
        # Validate the inputs
        errors = {}
        if hopes_and_dreams is not None and len(hopes_and_dreams) <= 5:
            errors["block_c"] = "The value must be longer than 5 characters"
        if len(errors) > 0:
            ack(response_action="errors", errors=errors)
            return
        # Acknowledge the view_submission event and close the modal
        ack()
        # Do whatever you want with the input data - here we're saving it to a DB
```

```python
    # Pass a function to this method
    app.view("view_1")(handle_submission)
```

Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload for details of payloads.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

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
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `view_submission` listener.
Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/`view_submission` for
details.

#### view\_closed

```python
def view_closed(
    constraints: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `view_closed` listener.
Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/`view_closed` for details.

#### options

```python
def options(
    constraints: Union[str, Pattern, Dict[str, Union[str, Pattern]]],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new options listener.
This method can be used as either a decorator or a method.

```python
    # Use this method as a decorator
    @app.options("menu_selection")
    def show_menu_options(ack):
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
        ack(options=options)
```

```python
    # Pass a function to this method
    app.options("menu_selection")(show_menu_options)
```

Refer to the following documents for details:

* https://docs.slack.dev/reference/block-kit/block-elements/select-menu-element#external_select
* https://docs.slack.dev/reference/block-kit/block-elements/multi-select-menu-element#external_multi_select

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.args`&#x27;s API document.

**Arguments**:

- `matchers` - A list of listener matcher functions.
  Only when all the matchers return True, the listener function can be invoked.
- `middleware` - A list of lister middleware functions.
  Only when all the middleware call `next()` method, the listener function can be invoked.

#### block\_suggestion

```python
def block_suggestion(
    action_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `block_suggestion` listener.

#### dialog\_suggestion

```python
def dialog_suggestion(
    callback_id: Union[str, Pattern],
    matchers: Optional[Sequence[Callable[..., bool]]] = None,
    middleware: Optional[Sequence[Union[Callable, Middleware]]] = None
) -> Callable[..., Optional[Callable[..., Optional[BoltResponse]]]]
```

Registers a new `dialog_suggestion` listener.
Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

#### default\_tokens\_revoked\_event\_listener

```python
def default_tokens_revoked_event_listener(
) -> Callable[..., Optional[BoltResponse]]
```

#### default\_app\_uninstalled\_event\_listener

```python
def default_app_uninstalled_event_listener(
) -> Callable[..., Optional[BoltResponse]]
```

#### enable\_token\_revocation\_listeners

```python
def enable_token_revocation_listeners() -> None
```

## BaseSocketModeHandler Objects

```python
class BaseSocketModeHandler()
```

#### app

#### client

#### handle

```python
def handle(client: BaseSocketModeClient, req: SocketModeRequest) -> None
```

Handles Socket Mode envelope requests through a WebSocket connection.

**Arguments**:

- `client` - this Socket Mode client instance
- `req` - the request data

#### connect

```python
def connect()
```

Establishes a new connection with the Socket Mode server

#### disconnect

```python
def disconnect()
```

Disconnects the current WebSocket connection with the Socket Mode server

#### close

```python
def close()
```

Disconnects from the Socket Mode server and cleans the resources this instance holds up

#### start

```python
def start()
```

Establishes a new connection and then blocks the current thread
to prevent the termination of this process.
If you don&#x27;t want to block the current thread, use ``connect()`` method instead.

#### run\_bolt\_app

```python
def run_bolt_app(app: App, req: SocketModeRequest)
```

#### send\_response

```python
def send_response(client: BaseSocketModeClient, req: SocketModeRequest,
                  bolt_resp: BoltResponse, start_time: float)
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

HTTP status code

#### body

The response body (dict and str are supported)

#### headers

The response headers.

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

## SocketModeHandler Objects

```python
class SocketModeHandler(BaseSocketModeHandler)
```

#### app

The Bolt app

#### app\_token

App-level token starting with `xapp-`

#### client

#### \_\_init\_\_

```python
def __init__(app: App,
             app_token: Optional[str] = None,
             logger: Optional[Logger] = None,
             web_client: Optional[WebClient] = None,
             ping_interval: float = 10,
             concurrency: int = 10,
             http_proxy_host: Optional[str] = None,
             http_proxy_port: Optional[int] = None,
             http_proxy_auth: Optional[Tuple[str, str]] = None,
             proxy_type: Optional[str] = None,
             trace_enabled: bool = False)
```

Socket Mode adapter for Bolt apps

**Arguments**:

- `app` - The Bolt app
- `app_token` - App-level token starting with `xapp-`
- `logger` - Custom logger
- `web_client` - custom `slack_sdk.web.WebClient` instance
- `ping_interval` - The ping-pong internal (seconds)
- `concurrency` - The size of the underlying thread pool
- `http_proxy_host` - HTTP proxy host
- `http_proxy_port` - HTTP proxy port
- `http_proxy_auth` - HTTP proxy authentication (username, password)
- `proxy_type` - Proxy type
- `trace_enabled` - True if trace-level logging is enabled

#### handle

```python
def handle(client: SocketModeClient, req: SocketModeRequest) -> None
```

