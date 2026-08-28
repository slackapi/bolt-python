---
sidebar_label: async_app
title: slack_bolt.async_app
---

Module for creating asyncio based apps.

### Creating an async app

If you'd prefer to build your app with [asyncio](https://docs.python.org/3/library/asyncio.html), you can import the [AIOHTTP](https://docs.aiohttp.org/en/stable/) library and call the `AsyncApp` constructor. Within async apps, you can use the async/await pattern.

```bash
# Python 3.7+ required
python -m venv .venv
source .venv/bin/activate

pip install -U pip
# aiohttp is required
pip install slack_bolt aiohttp
```

In async apps, all middleware/listeners must be async functions. When calling utility methods (like `ack` and `say`) within these functions, it's required to use the `await` keyword.

```python
# Import the async app instead of the regular one
from slack_bolt.async_app import AsyncApp

app = AsyncApp()

@app.event("app_mention")
async def event_test(body, say, logger):
    logger.info(body)
    await say("What's up?")

@app.command("/hello-bolt-python")
async def command(ack, body, respond):
    await ack()
    await respond(f"Hi <@{body['user_id']}>!")

if __name__ == "__main__":
    app.start(3000)
```

If you want to use another async Web framework (e.g., Sanic, FastAPI, Starlette), take a look at the built-in adapters and their examples.

* [The Bolt app examples](https://github.com/slackapi/bolt-python/tree/main/examples)
* [The built-in adapters](https://github.com/slackapi/bolt-python/tree/main/slack_bolt/adapter)
Apps can be run the same way as the synchronous example above. If you'd prefer another async Web framework (e.g., Sanic, FastAPI, Starlette), take a look at [the built-in adapters](https://github.com/slackapi/bolt-python/tree/main/slack_bolt/adapter) and their corresponding [examples](https://github.com/slackapi/bolt-python/tree/main/examples).

Refer to `slack_bolt.app.async_app` for more details.

## `AsyncApp`

```python
AsyncApp(*, logger=None, name=None, process_before_response=False, raise_error_for_unhandled_request=False, signing_secret=None, token=None, client=None, before_authorize=None, authorize=None, user_facing_authorize_error_message=None, installation_store=None, installation_store_bot_only=None, request_verification_enabled=True, ignoring_self_events_enabled=True, ignoring_self_assistant_message_events_enabled=True, ssl_check_enabled=True, url_verification_enabled=True, attaching_function_token_enabled=True, oauth_settings=None, oauth_flow=None, verification_token=None, assistant_thread_context_store=None, attaching_conversation_kwargs_enabled=True)
```

Bolt App that provides functionalities to register middleware/listeners.

```python
import os
from slack_bolt.async_app import AsyncApp

# Initializes your app with your bot token and signing secret
app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))


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

**Parameters:**

- **logger** (Optional[Logger]) – The custom logger that can be used in this app.
- **name** (Optional[str]) – The application name that will be used in logging. If absent, the source file name will be used.
- **process_before_response** (bool) – True if this app runs on Function as a Service. (Default: False)
- **raise_error_for_unhandled_request** (bool) – True if you want to raise exceptions for unhandled requests
and use @app.error listeners instead of
the built-in handler, which pints warning logs and returns 404 to Slack (Default: False)
- **signing_secret** (Optional[str]) – The Signing Secret value used for verifying requests from Slack.
- **token** (Optional[str]) – The bot/user access token required only for single-workspace app.
- **client** (Optional[AsyncWebClient]) – The singleton `slack_sdk.web.async_client.AsyncWebClient` instance for this app.
- **before_authorize** (Optional[Union[AsyncMiddleware, Callable..., [Awaitable[Any]]]]) – A global middleware that can be executed right before authorize function
- **authorize** (Optional[Callable..., [Awaitable[AuthorizeResult]]]) – The function to authorize an incoming request from Slack
by checking if there is a team/user in the installation data.
- **user_facing_authorize_error_message** (Optional[str]) – The user-facing error message to display
when the app is installed but the installation is not managed by this app's installation store
- **installation_store** (Optional[AsyncInstallationStore]) – The module offering save/find operations of installation data
- **installation_store_bot_only** (Optional[bool]) – Use `AsyncInstallationStore#async_find_bot()` if True (Default: False)
- **request_verification_enabled** (bool) – False if you would like to disable the built-in middleware (Default: True).
`AsyncRequestVerification` is a built-in middleware that verifies the signature in HTTP Mode requests.
Make sure if it's safe enough when you turn a built-in middleware off.
We strongly recommend using RequestVerification for better security.
If you have a proxy that verifies request signature in front of the Bolt app,
it's totally fine to disable RequestVerification to avoid duplication of work.
Don't turn it off just for easiness of development.
- **ignoring_self_events_enabled** (bool) – False if you would like to disable the built-in middleware (Default: True).
`AsyncIgnoringSelfEvents` is a built-in middleware that enables Bolt apps to easily skip the events
generated by this app's bot user (this is useful for avoiding code error causing an infinite loop).
- **ignoring_self_assistant_message_events_enabled** (bool) – False if you would like to disable the built-in middleware.
`IgnoringSelfEvents` for this app's bot user message events within an assistant thread
This is useful for avoiding code error causing an infinite loop; Default: True
- **url_verification_enabled** (bool) – False if you would like to disable the built-in middleware (Default: True).
`AsyncUrlVerification` is a built-in middleware that handles url_verification requests
that verify the endpoint for Events API in HTTP Mode requests.
- **ssl_check_enabled** (bool) – bool = False if you would like to disable the built-in middleware (Default: True).
`AsyncSslCheck` is a built-in middleware that handles ssl_check requests from Slack.
- **attaching_function_token_enabled** (bool) – False if you would like to disable the built-in middleware (Default: True).
`AsyncAttachingFunctionToken` is a built-in middleware that injects the just-in-time workflow-execution token
when your app receives `function_executed` or interactivity events scoped to a custom step.
- **oauth_settings** (Optional[AsyncOAuthSettings]) – The settings related to Slack app installation flow (OAuth flow)
- **oauth_flow** (Optional[AsyncOAuthFlow]) – Instantiated `slack_bolt.oauth.AsyncOAuthFlow`. This is always prioritized over oauth_settings.
- **verification_token** (Optional[str]) – Deprecated verification mechanism. This can be used only for ssl_check requests.
- **assistant_thread_context_store** (Optional[AsyncAssistantThreadContextStore]) – Custom AssistantThreadContext store (Default: the built-in implementation,
which uses a parent message's metadata to store the latest context)
- **attaching_conversation_kwargs_enabled** (bool) – False if you would like to disable the built-in
middleware (Default: True). `AttachingConversationKwargs` is a built-in middleware that attaches
conversation-specific listener arguments (such as `say`, `set_status`, `say_stream`, and
`set_suggested_prompts`) for assistant thread and direct message events.

### `action`

```python
action(constraints, matchers=None, middleware=None)
```

Registers a new action listener. This method can be used as either a decorator or a method.

```python
# Use this method as a decorator
@app.action("approve_button")
async def update_message(ack):
    await ack()


# Pass a function to this method
app.action("approve_button")(update_message)
```

* Refer to https://docs.slack.dev/reference/interaction-payloads/block_actions-payload/ for actions in `blocks`.
* Refer to https://docs.slack.dev/legacy/legacy-messaging/legacy-message-buttons/ for actions in `attachments`.
* Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for actions in dialogs.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **constraints** (Union[str, Pattern, Dict[str, Union[str, Pattern]]]) – The conditions that match a request payload
- **matchers** (Optional[Sequence[Callable..., [Awaitable[bool]]]]) – A list of listener matcher functions.
Only when all the matchers return True, the listener function can be invoked.
- **middleware** (Optional[Sequence[Union[Callable, AsyncMiddleware]]]) – A list of lister middleware functions.
Only when all the middleware call `next()` method, the listener function can be invoked.

### `async_dispatch`

```python
async_dispatch(req)
```

Applies all middleware and dispatches an incoming request from Slack to the right code path.

**Parameters:**

- **req** (AsyncBoltRequest) – An incoming request from Slack.

**Returns:**

- BoltResponse – The response generated by this Bolt app.

### `attachment_action`

```python
attachment_action(callback_id, matchers=None, middleware=None)
```

Registers a new `interactive_message` action listener.

Refer to https://docs.slack.dev/legacy/legacy-messaging/legacy-message-buttons/ for details.

### `block_action`

```python
block_action(constraints, matchers=None, middleware=None)
```

Registers a new `block_actions` action listener.

Refer to https://docs.slack.dev/reference/interaction-payloads/block_actions-payload/ for details.

### `block_suggestion`

```python
block_suggestion(action_id, matchers=None, middleware=None)
```

Registers a new `block_suggestion` listener.

### `client`

```python
client: AsyncWebClient
```

The singleton `slack_sdk.web.async_client.AsyncWebClient` instance in this app.

### `command`

```python
command(command, matchers=None, middleware=None)
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


# Pass a function to this method
app.command("/echo")(repeat_text)
```

Refer to https://docs.slack.dev/interactivity/implementing-slash-commands/ for details of Slash Commands.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **command** (Union[str, Pattern]) – The conditions that match a request payload
- **matchers** (Optional[Sequence[Callable..., [Awaitable[bool]]]]) – A list of listener matcher functions.
Only when all the matchers return True, the listener function can be invoked.
- **middleware** (Optional[Sequence[Union[Callable, AsyncMiddleware]]]) – A list of lister middleware functions.
Only when all the middleware call `next()` method, the listener function can be invoked.

### `dialog_cancellation`

```python
dialog_cancellation(callback_id, matchers=None, middleware=None)
```

Registers a new `dialog_cancellation` listener.

Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

### `dialog_submission`

```python
dialog_submission(callback_id, matchers=None, middleware=None)
```

Registers a new `dialog_submission` listener.

Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

### `dialog_suggestion`

```python
dialog_suggestion(callback_id, matchers=None, middleware=None)
```

Registers a new `dialog_suggestion` listener.

Refer to https://docs.slack.dev/legacy/legacy-dialogs/ for details.

### `error`

```python
error(func)
```

Updates the global error handler. This method can be used as either a decorator or a method.

```python
# Use this method as a decorator
@app.error
async def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")


# Pass a function to this method
app.error(custom_error_handler)
```

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **func** (Callable..., [Awaitable[Optional[BoltResponse]]]) – The function that is supposed to be executed
when getting an unhandled error in Bolt app.

### `event`

```python
event(event, matchers=None, middleware=None)
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


# Pass a function to this method
app.event("team_join")(ask_for_introduction)
```

Refer to https://docs.slack.dev/apis/events-api/ for details of Events API.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **event** (Union[str, Pattern, Dict[str, Optional[Union[str, Sequence[Optional[Union[str, Pattern]]]]]]]) – The conditions that match a request payload.
If you pass a dict for this, you can have type, subtype in the constraint.
- **matchers** (Optional[Sequence[Callable..., [Awaitable[bool]]]]) – A list of listener matcher functions.
Only when all the matchers return True, the listener function can be invoked.
- **middleware** (Optional[Sequence[Union[Callable, AsyncMiddleware]]]) – A list of lister middleware functions.
Only when all the middleware call `next()` method, the listener function can be invoked.

### `function`

```python
function(callback_id, matchers=None, middleware=None, auto_acknowledge=True, ack_timeout=3)
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


# Pass a function to this method
app.function("reverse")(reverse_string)
```

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **callback_id** (Union[str, Pattern]) – The callback id to identify the function
- **matchers** (Optional[Sequence[Callable..., [Awaitable[bool]]]]) – A list of listener matcher functions.
Only when all the matchers return True, the listener function can be invoked.
- **middleware** (Optional[Sequence[Union[Callable, AsyncMiddleware]]]) – A list of lister middleware functions.
Only when all the middleware call `next()` method, the listener function can be invoked.
- **auto_acknowledge** (bool) – Whether Bolt automatically acknowledges the function execution event on the
listener's behalf. When False, your listener must call `ack()` itself within `ack_timeout`
seconds (Default: True).
- **ack_timeout** (int) – The number of seconds to wait for the listener to call `ack()`.
Only takes effect when `auto_acknowledge` is False (Default: 3).

### `global_shortcut`

```python
global_shortcut(callback_id, matchers=None, middleware=None)
```

Registers a new global shortcut listener.

### `installation_store`

```python
installation_store: Optional[AsyncInstallationStore]
```

The `slack_sdk.oauth.AsyncInstallationStore` that can be used in the `authorize` middleware.

### `listener_runner`

```python
listener_runner: AsyncioListenerRunner
```

The asyncio-based executor for asynchronously running listeners.

### `logger`

```python
logger: logging.Logger
```

The logger this app uses.

### `message`

```python
message(keyword='', matchers=None, middleware=None)
```

Registers a new message event listener. This method can be used as either a decorator or a method.

Check the `App#event` method's docstring for details.

```python
# Use this method as a decorator
@app.message(":wave:")
async def say_hello(message, say):
    user = message["user"]
    await say(f"Hi there, <@{user}>!")


# Pass a function to this method
app.message(":wave:")(say_hello)
```

Refer to https://docs.slack.dev/reference/events/message/ for details of `message` events.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **keyword** (Union[str, Pattern]) – The keyword to match
- **matchers** (Optional[Sequence[Callable..., [Awaitable[bool]]]]) – A list of listener matcher functions.
Only when all the matchers return True, the listener function can be invoked.
- **middleware** (Optional[Sequence[Union[Callable, AsyncMiddleware]]]) – A list of lister middleware functions.
Only when all the middleware call `next()` method, the listener function can be invoked.

### `message_shortcut`

```python
message_shortcut(callback_id, matchers=None, middleware=None)
```

Registers a new message shortcut listener.

### `middleware`

```python
middleware(*args)
```

Registers a new middleware to this app.

This method can be used as either a decorator or a method.

```python
# Use this method as a decorator
@app.middleware
async def middleware_func(logger, body, next):
    logger.info(f"request body: {body}")
    await next()


# Pass a function to this method
app.middleware(middleware_func)
```

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- ***args** – A function that works as a global middleware.

### `name`

```python
name: str
```

The name of this app (default: the filename).

### `oauth_flow`

```python
oauth_flow: Optional[AsyncOAuthFlow]
```

Configured `OAuthFlow` object if exists.

### `options`

```python
options(constraints, matchers=None, middleware=None)
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


# Pass a function to this method
app.options("menu_selection")(show_menu_options)
```

Refer to the following documents for details:

* https://docs.slack.dev/reference/block-kit/block-elements/select-menu-element#external_select
* https://docs.slack.dev/reference/block-kit/block-elements/multi-select-menu-element#external_multi_select

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **constraints** (Union[str, Pattern, Dict[str, Union[str, Pattern]]]) – The conditions that match a request payload
- **matchers** (Optional[Sequence[Callable..., [Awaitable[bool]]]]) – A list of listener matcher functions.
Only when all the matchers return True, the listener function can be invoked.
- **middleware** (Optional[Sequence[Union[Callable, AsyncMiddleware]]]) – A list of lister middleware functions.
Only when all the middleware call `next()` method, the listener function can be invoked.

### `server`

```python
server(port=3000, path='/slack/events', host=None)
```

Configure a web server using AIOHTTP.

Refer to https://docs.aiohttp.org/ for more details about AIOHTTP.

**Parameters:**

- **port** (int) – The port to listen on (Default: 3000)
- **path** (str) – The path to handle request from Slack (Default: `/slack/events`)
- **host** (Optional[str]) – The hostname to serve the web endpoints. (Default: 0.0.0.0)

### `shortcut`

```python
shortcut(constraints, matchers=None, middleware=None)
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
        view={...},
    )


# Pass a function to this method
app.shortcut("open_modal")(open_modal)
```

Refer to https://docs.slack.dev/interactivity/implementing-shortcuts/ for details about Shortcuts.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **constraints** (Union[str, Pattern, Dict[str, Union[str, Pattern]]]) – The conditions that match a request payload.
- **matchers** (Optional[Sequence[Callable..., [Awaitable[bool]]]]) – A list of listener matcher functions.
Only when all the matchers return True, the listener function can be invoked.
- **middleware** (Optional[Sequence[Union[Callable, AsyncMiddleware]]]) – A list of lister middleware functions.
Only when all the middleware call `next()` method, the listener function can be invoked.

### `start`

```python
start(port=3000, path='/slack/events', host=None)
```

Start a web server using AIOHTTP.

Refer to https://docs.aiohttp.org/ for more details about AIOHTTP.

**Parameters:**

- **port** (int) – The port to listen on (Default: 3000)
- **path** (str) – The path to handle request from Slack (Default: `/slack/events`)
- **host** (Optional[str]) – The hostname to serve the web endpoints. (Default: 0.0.0.0)

### `step`

```python
step(callback_id, edit=None, save=None, execute=None)
```

Deprecated: register a new step from app listener.

Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new step from app listener.

Unlike others, this method doesn't behave as a decorator.
If you want to register a step from app by a decorator, use `AsyncWorkflowStepBuilder`'s methods.

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

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.
For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Parameters:**

- **callback_id** (Union[str, Pattern, AsyncWorkflowStep, AsyncWorkflowStepBuilder]) – The Callback ID for this step from app
- **edit** (Optional[Union[Callable..., [Optional[BoltResponse]], AsyncListener, Sequence[Callable]]]) – The function for displaying a modal in the Workflow Builder
- **save** (Optional[Union[Callable..., [Optional[BoltResponse]], AsyncListener, Sequence[Callable]]]) – The function for handling configuration in the Workflow Builder
- **execute** (Optional[Union[Callable..., [Optional[BoltResponse]], AsyncListener, Sequence[Callable]]]) – The function for handling the step execution

### `use`

```python
use(*args)
```

Refer to `AsyncApp#middleware()` method's docstring for details.

### `view`

```python
view(constraints, matchers=None, middleware=None)
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
        return  # Return early to display the validation errors to the user
    # Acknowledge the view_submission event and close the modal
    await ack()
    # Do whatever you want with the input data - here we're saving it to a DB


# Pass a function to this method
app.view("view_1")(handle_submission)
```

Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload for details of payloads.

To learn available arguments for middleware/listeners, see `slack_bolt.kwargs_injection.async_args`'s API document.

**Parameters:**

- **constraints** (Union[str, Pattern, Dict[str, Union[str, Pattern]]]) – The conditions that match a request payload
- **matchers** (Optional[Sequence[Callable..., [Awaitable[bool]]]]) – A list of listener matcher functions.
Only when all the matchers return True, the listener function can be invoked.
- **middleware** (Optional[Sequence[Union[Callable, AsyncMiddleware]]]) – A list of lister middleware functions.
Only when all the middleware call `next()` method, the listener function can be invoked.

### `view_closed`

```python
view_closed(constraints, matchers=None, middleware=None)
```

Registers a new `view_closed` listener.

Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/#view_closed for details.

### `view_submission`

```python
view_submission(constraints, matchers=None, middleware=None)
```

Registers a new `view_submission` listener.

Refer to https://docs.slack.dev/reference/interaction-payloads/view-interactions-payload/#view_submission for
details.

### `web_app`

```python
web_app(path='/slack/events', port=3000)
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

**Parameters:**

- **path** (str) – The path to receive incoming requests from Slack
- **port** (int) – The port to listen on (Default: 3000)

## `AsyncBoltContext`

Bases: BaseContext

Context object associated with a request from Slack.

### `ack`

```python
ack: AsyncAck
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

**Returns:**

- AsyncAck – Callable `ack()` function

### `actor_enterprise_id`

```python
actor_enterprise_id: Optional[str]
```

The action's actor's Enterprise Grid organization ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `actor_team_id`

```python
actor_team_id: Optional[str]
```

The action's actor's workspace ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `actor_user_id`

```python
actor_user_id: Optional[str]
```

The action's actor's user ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `authorize_result`

```python
authorize_result: Optional[AuthorizeResult]
```

The authorize result resolved for this request.

### `bot_id`

```python
bot_id: Optional[str]
```

The bot ID resolved for this request.

### `bot_token`

```python
bot_token: Optional[str]
```

The bot token resolved for this request.

### `bot_user_id`

```python
bot_user_id: Optional[str]
```

The bot user ID resolved for this request.

### `channel_id`

```python
channel_id: Optional[str]
```

The conversation ID associated with this request.

### `client`

```python
client: AsyncWebClient
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

**Returns:**

- AsyncWebClient – `AsyncWebClient` instance

### `complete`

```python
complete: AsyncComplete
```

`complete()` function for this request.

Once a custom function's state is set to complete,
any outputs the function returns will be passed along to the next step of its housing workflow,
or complete the workflow if the function is the last step in a workflow. Additionally,
any interactivity handlers associated to a function invocation will no longer be invocable.

```python
@app.function("reverse")
async def handle_button_clicks(ack, complete):
    await ack()
    await complete(outputs={"stringReverse": "olleh"})


@app.function("reverse")
async def handle_button_clicks(context):
    await context.ack()
    await context.complete(outputs={"stringReverse": "olleh"})
```

**Returns:**

- AsyncComplete – Callable `complete()` function

### `enterprise_id`

```python
enterprise_id: Optional[str]
```

The Enterprise Grid Organization ID of this request.

### `fail`

```python
fail: AsyncFail
```

`fail()` function for this request.

Once a custom function's state is set to error,
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

**Returns:**

- AsyncFail – Callable `fail()` function

### `function_bot_access_token`

```python
function_bot_access_token: Optional[str]
```

The bot token resolved for this function request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `function_execution_id`

```python
function_execution_id: Optional[str]
```

The `function_execution_id` associated with this request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `inputs`

```python
inputs: Optional[Dict[str, Any]]
```

The `inputs` associated with this request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `is_enterprise_install`

```python
is_enterprise_install: Optional[bool]
```

True if the request is associated with an Org-wide installation.

### `listener_runner`

```python
listener_runner: AsyncioListenerRunner
```

The properly configured listener_runner that is available for middleware/listeners.

### `logger`

```python
logger: Logger
```

The properly configured logger that is available for middleware/listeners.

### `matches`

```python
matches: Optional[Tuple]
```

Returns all the matched parts in message listener's regexp.

### `respond`

```python
respond: Optional[AsyncRespond]
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

**Returns:**

- Optional[AsyncRespond] – Callable `respond()` function

### `response_url`

```python
response_url: Optional[str]
```

The `response_url` associated with this request.

### `say`

```python
say: AsyncSay
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

**Returns:**

- AsyncSay – Callable `say()` function

### `team_id`

```python
team_id: Optional[str]
```

The Workspace ID of this request.

### `thread_ts`

```python
thread_ts: Optional[str]
```

The conversation thread's ID associated with this request.

### `token`

```python
token: Optional[str]
```

The (bot/user) token resolved for this request.

### `user_id`

```python
user_id: Optional[str]
```

The user ID associated ith this request.

### `user_token`

```python
user_token: Optional[str]
```

The user token resolved for this request.

## `AsyncBoltRequest`

```python
AsyncBoltRequest(*, body, query=None, headers=None, context=None, mode='http')
```

Request to a Bolt app.

**Parameters:**

- **body** (Union[str, dict]) – The raw request body (only plain text is supported for "http" mode)
- **query** (Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]]) – The query string data in any data format.
- **headers** (Optional[Dict[str, Union[str, Sequence[str]]]]) – The request headers.
- **context** (Optional[Dict[str, Any]]) – The context in this request.
- **mode** (str) – The mode used for this request. (either "http" or "socket_mode")

## `AsyncListener`

### `run_ack_function`

```python
run_ack_function(*, request, response)
```

Runs all the registered middleware and then run the listener function.

**Parameters:**

- **request** (AsyncBoltRequest) – The incoming request
- **response** (BoltResponse) – The current response

**Returns:**

- Optional[BoltResponse] – The processed response

### `run_async_middleware`

```python
run_async_middleware(*, req, resp)
```

Runs an async middleware.

**Parameters:**

- **req** (AsyncBoltRequest) – The incoming request
- **resp** (BoltResponse) – The current response

**Returns:**

- Tuple[Optional[BoltResponse], bool] – A tuple of the processed response and a flag indicating termination

## `AsyncSayStream`

```python
AsyncSayStream(*, client, channel=None, recipient_team_id=None, recipient_user_id=None, thread_ts=None)
```
