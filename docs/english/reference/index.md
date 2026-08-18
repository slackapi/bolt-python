---
sidebar_label: slack_bolt
title: slack_bolt
---


A Python framework to build Slack apps in a flash with the latest platform features.Read the [getting started guide](https://docs.slack.dev/tools/bolt-python/creating-an-app) and look at our [code examples](https://github.com/slackapi/bolt-python/tree/main/examples) to learn how to build apps using Bolt.

* Website: https://docs.slack.dev/tools/bolt-python/
* GitHub repository: https://github.com/slackapi/bolt-python
* The class representing a Bolt app: `slack_bolt.app.app`

## Submodules

- [slack_bolt.adapter](/tools/bolt-python/reference/adapter)
- [slack_bolt.app](/tools/bolt-python/reference/app)
- [slack_bolt.async_app](/tools/bolt-python/reference/async_app)
- [slack_bolt.authorization](/tools/bolt-python/reference/authorization)
- [slack_bolt.context](/tools/bolt-python/reference/context)
- [slack_bolt.error](/tools/bolt-python/reference/error)
- [slack_bolt.kwargs_injection](/tools/bolt-python/reference/kwargs_injection)
- [slack_bolt.lazy_listener](/tools/bolt-python/reference/lazy_listener)
- [slack_bolt.listener](/tools/bolt-python/reference/listener)
- [slack_bolt.listener_matcher](/tools/bolt-python/reference/listener_matcher)
- [slack_bolt.logger](/tools/bolt-python/reference/logger)
- [slack_bolt.middleware](/tools/bolt-python/reference/middleware)
- [slack_bolt.oauth](/tools/bolt-python/reference/oauth)
- [slack_bolt.request](/tools/bolt-python/reference/request)
- [slack_bolt.response](/tools/bolt-python/reference/response)
- [slack_bolt.util](/tools/bolt-python/reference/util)
- [slack_bolt.version](/tools/bolt-python/reference/version)
- [slack_bolt.workflows](/tools/bolt-python/reference/workflows)

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

#### \_\_init\_\_

```python
def __init__()
```

## Complete Objects

```python
class Complete()
```

#### client

#### function\_execution\_id

#### \_\_init\_\_

```python
def __init__(client: WebClient, function_execution_id: Optional[str])
```

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

#### \_\_init\_\_

```python
def __init__(client: WebClient, function_execution_id: Optional[str])
```

#### has\_been\_called

```python
def has_been_called() -> bool
```

Check if this fail function has been called.

**Returns**:

- `bool` - True if the fail function has been called, False otherwise.

## Respond Objects

```python
class Respond()
```

#### response\_url

#### proxy

#### ssl

#### \_\_init\_\_

```python
def __init__(*,
             response_url: Optional[str],
             proxy: Optional[str] = None,
             ssl: Optional[SSLContext] = None)
```

## Say Objects

```python
class Say()
```

#### client

#### channel

#### thread\_ts

#### metadata

#### build\_metadata

#### \_\_init\_\_

```python
def __init__(
    client: Optional[WebClient],
    channel: Optional[str],
    thread_ts: Optional[str] = None,
    metadata: Optional[Union[Dict, Metadata]] = None,
    build_metadata: Optional[Callable[[], Optional[Union[Dict,
                                                         Metadata]]]] = None)
```

## SayStream Objects

```python
class SayStream()
```

#### client

#### channel

#### recipient\_team\_id

#### recipient\_user\_id

#### thread\_ts

#### \_\_init\_\_

```python
def __init__(*,
             client: WebClient,
             channel: Optional[str] = None,
             recipient_team_id: Optional[str] = None,
             recipient_user_id: Optional[str] = None,
             thread_ts: Optional[str] = None)
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

#### \_\_init\_\_

```python
def __init__(*,
             logger: logging.Logger,
             client: WebClient,
             req: BoltRequest,
             resp: BoltResponse,
             context: BoltContext,
             body: Dict[str, Any],
             payload: Dict[str, Any],
             options: Optional[Dict[str, Any]] = None,
             shortcut: Optional[Dict[str, Any]] = None,
             action: Optional[Dict[str, Any]] = None,
             view: Optional[Dict[str, Any]] = None,
             command: Optional[Dict[str, Any]] = None,
             event: Optional[Dict[str, Any]] = None,
             message: Optional[Dict[str, Any]] = None,
             ack: Ack,
             say: Say,
             respond: Respond,
             complete: Complete,
             fail: Fail,
             set_status: Optional[SetStatus] = None,
             set_title: Optional[SetTitle] = None,
             set_suggested_prompts: Optional[SetSuggestedPrompts] = None,
             get_thread_context: Optional[GetThreadContext] = None,
             save_thread_context: Optional[SaveThreadContext] = None,
             say_stream: Optional[SayStream] = None,
             next: Callable[[], None],
             **kwargs)
```

## Listener Objects

```python
class Listener(metaclass=ABCMeta)
```

#### matchers

#### middleware

#### ack\_function

#### lazy\_functions

#### auto\_acknowledgement

#### ack\_timeout

#### matches

```python
def matches(*, req: BoltRequest, resp: BoltResponse) -> bool
```

#### run\_middleware

```python
def run_middleware(*, req: BoltRequest,
                   resp: BoltResponse) -> Tuple[Optional[BoltResponse], bool]
```

Runs a middleware.

**Arguments**:

- `req` - The incoming request
- `resp` - The current response
  

**Returns**:

  A tuple of the processed response and a flag indicating termination

#### run\_ack\_function

```python
@abstractmethod
def run_ack_function(*, request: BoltRequest,
                     response: BoltResponse) -> Optional[BoltResponse]
```

Runs all the registered middleware and then run the listener function.

**Arguments**:

- `request` - The incoming request
- `response` - The current response
  

**Returns**:

  The processed response

## CustomListenerMatcher Objects

```python
class CustomListenerMatcher(ListenerMatcher)
```

#### app\_name

#### func

#### arg\_names

#### logger

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             func: Callable[..., bool],
             base_logger: Optional[Logger] = None)
```

#### matches

```python
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

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
def to_copyable() -> "BoltRequest"
```

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

## Assistant Objects

```python
class Assistant(Middleware)
```

#### thread\_context\_store

#### base\_logger

#### \_\_init\_\_

```python
def __init__(
        *,
        app_name: str = "assistant",
        thread_context_store: Optional[AssistantThreadContextStore] = None,
        logger: Optional[logging.Logger] = None)
```

#### thread\_started

```python
def thread_started(*args,
                   matchers: Optional[Union[Callable[..., bool],
                                            ListenerMatcher]] = None,
                   middleware: Optional[Union[Callable, Middleware]] = None,
                   lazy: Optional[List[Callable[..., None]]] = None)
```

#### user\_message

```python
def user_message(*args,
                 matchers: Optional[Union[Callable[..., bool],
                                          ListenerMatcher]] = None,
                 middleware: Optional[Union[Callable, Middleware]] = None,
                 lazy: Optional[List[Callable[..., None]]] = None)
```

#### bot\_message

```python
def bot_message(*args,
                matchers: Optional[Union[Callable[..., bool],
                                         ListenerMatcher]] = None,
                middleware: Optional[Union[Callable, Middleware]] = None,
                lazy: Optional[List[Callable[..., None]]] = None)
```

#### thread\_context\_changed

```python
def thread_context_changed(*args,
                           matchers: Optional[Union[Callable[..., bool],
                                                    ListenerMatcher]] = None,
                           middleware: Optional[Union[Callable,
                                                      Middleware]] = None,
                           lazy: Optional[List[Callable[..., None]]] = None)
```

#### default\_thread\_context\_changed

```python
@staticmethod
def default_thread_context_changed(save_thread_context: SaveThreadContext,
                                   payload: dict)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

#### build\_listener

```python
def build_listener(listener_or_functions: Union[Listener, Callable,
                                                List[Callable]],
                   matchers: Optional[List[Union[ListenerMatcher,
                                                 Callable[..., bool]]]] = None,
                   middleware: Optional[List[Middleware]] = None,
                   base_logger: Optional[Logger] = None) -> Listener
```

## AssistantThreadContext Objects

```python
class AssistantThreadContext(dict)
```

#### enterprise\_id

#### team\_id

#### channel\_id

#### \_\_init\_\_

```python
def __init__(payload: dict)
```

## AssistantThreadContextStore Objects

```python
class AssistantThreadContextStore()
```

#### save

```python
def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
def find(*, channel_id: str,
         thread_ts: str) -> Optional[AssistantThreadContext]
```

## FileAssistantThreadContextStore Objects

```python
class FileAssistantThreadContextStore(AssistantThreadContextStore)
```

#### \_\_init\_\_

```python
def __init__(base_dir: str = str(Path.home()) +
             "/.bolt-app-assistant-thread-contexts")
```

#### save

```python
def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
def find(*, channel_id: str,
         thread_ts: str) -> Optional[AssistantThreadContext]
```

## SetStatus Objects

```python
class SetStatus()
```

#### client

#### channel\_id

#### thread\_ts

#### \_\_init\_\_

```python
def __init__(client: WebClient, channel_id: str, thread_ts: str)
```

## SetTitle Objects

```python
class SetTitle()
```

#### client

#### channel\_id

#### thread\_ts

#### \_\_init\_\_

```python
def __init__(client: WebClient, channel_id: str, thread_ts: str)
```

## SetSuggestedPrompts Objects

```python
class SetSuggestedPrompts()
```

#### client

#### channel\_id

#### thread\_ts

#### \_\_init\_\_

```python
def __init__(client: WebClient,
             channel_id: str,
             thread_ts: Optional[str] = None)
```

## SaveThreadContext Objects

```python
class SaveThreadContext()
```

#### thread\_context\_store

#### channel\_id

#### thread\_ts

#### \_\_init\_\_

```python
def __init__(thread_context_store: AssistantThreadContextStore,
             channel_id: str, thread_ts: str)
```

