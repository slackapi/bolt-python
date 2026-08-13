---
sidebar_label: async_app
title: slack_bolt.app.async_app
---

## AsyncSlackAppServer Objects

```python
class AsyncSlackAppServer()
```

#### port

#### path

#### host

#### bolt\_app

#### web\_app

#### handle\_get\_requests

```python
async def handle_get_requests(request: web.Request) -> web.Response
```

#### handle\_post\_requests

```python
async def handle_post_requests(request: web.Request) -> web.Response
```

#### start

```python
def start(host: Optional[str] = None) -> None
```

Starts a new web server process.

## AsyncAssistantThreadContextStore Objects

```python
class AsyncAssistantThreadContextStore()
```

#### save

```python
async def save(*, channel_id: str, thread_ts: str, context: Dict[str,
                                                                 str]) -> None
```

#### find

```python
async def find(*, channel_id: str,
               thread_ts: str) -> Optional[AssistantThreadContext]
```

## AsyncTokenRevocationListeners Objects

```python
class AsyncTokenRevocationListeners()
```

Listener functions to handle token revocation / uninstallation events

#### installation\_store

#### handle\_tokens\_revoked\_events

```python
async def handle_tokens_revoked_events(event: dict,
                                       context: AsyncBoltContext) -> None
```

#### handle\_app\_uninstalled\_events

```python
async def handle_app_uninstalled_events(context: AsyncBoltContext) -> None
```

## AsyncDefaultListenerStartHandler Objects

```python
class AsyncDefaultListenerStartHandler(AsyncListenerStartHandler)
```

#### handle

```python
async def handle(request: AsyncBoltRequest, response: Optional[BoltResponse])
```

## AsyncDefaultListenerCompletionHandler Objects

```python
class AsyncDefaultListenerCompletionHandler(AsyncListenerCompletionHandler)
```

#### handle

```python
async def handle(request: AsyncBoltRequest, response: Optional[BoltResponse])
```

## AsyncioListenerRunner Objects

```python
class AsyncioListenerRunner()
```

#### logger

#### process\_before\_response

#### listener\_error\_handler

#### listener\_start\_handler

#### listener\_completion\_handler

#### lazy\_listener\_runner

#### run

```python
async def run(request: AsyncBoltRequest,
              response: BoltResponse,
              listener_name: str,
              listener: AsyncListener,
              starting_time: Optional[float] = None) -> Optional[BoltResponse]
```

## AsyncAssistant Objects

```python
class AsyncAssistant(AsyncMiddleware)
```

#### thread\_context\_store

#### base\_logger

#### thread\_started

```python
def thread_started(*args,
                   matchers: Optional[Union[Callable[..., bool],
                                            AsyncListenerMatcher]] = None,
                   middleware: Optional[Union[Callable,
                                              AsyncMiddleware]] = None,
                   lazy: Optional[List[Callable[..., None]]] = None)
```

#### user\_message

```python
def user_message(*args,
                 matchers: Optional[Union[Callable[..., bool],
                                          AsyncListenerMatcher]] = None,
                 middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
                 lazy: Optional[List[Callable[..., None]]] = None)
```

#### bot\_message

```python
def bot_message(*args,
                matchers: Optional[Union[Callable[..., bool],
                                         AsyncListenerMatcher]] = None,
                middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
                lazy: Optional[List[Callable[..., None]]] = None)
```

#### thread\_context\_changed

```python
def thread_context_changed(
        *args,
        matchers: Optional[Union[Callable[..., bool],
                                 AsyncListenerMatcher]] = None,
        middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
        lazy: Optional[List[Callable[..., None]]] = None)
```

#### default\_thread\_context\_changed

```python
@staticmethod
async def default_thread_context_changed(
        save_thread_context: AsyncSaveThreadContext, payload: dict)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

#### build\_listener

```python
def build_listener(listener_or_functions: Union[AsyncListener, Callable,
                                                List[Callable]],
                   matchers: Optional[List[
                       Union[AsyncListenerMatcher,
                             Callable[..., Awaitable[bool]]]]] = None,
                   middleware: Optional[List[AsyncMiddleware]] = None,
                   base_logger: Optional[Logger] = None) -> AsyncListener
```

## AsyncCustomMiddlewareErrorHandler Objects

```python
class AsyncCustomMiddlewareErrorHandler(AsyncMiddlewareErrorHandler)
```

#### handle

```python
async def handle(error: Exception, request: AsyncBoltRequest,
                 response: Optional[BoltResponse]) -> None
```

## AsyncDefaultMiddlewareErrorHandler Objects

```python
class AsyncDefaultMiddlewareErrorHandler(AsyncMiddlewareErrorHandler)
```

#### handle

```python
async def handle(error: Exception, request: AsyncBoltRequest,
                 response: Optional[BoltResponse])
```

## AsyncMiddlewareErrorHandler Objects

```python
class AsyncMiddlewareErrorHandler(metaclass=ABCMeta)
```

#### handle

```python
@abstractmethod
async def handle(error: Exception, request: AsyncBoltRequest,
                 response: Optional[BoltResponse]) -> None
```

Handles an unhandled exception.

**Arguments**:

- `error` - The raised exception.
- `request` - The request.
- `response` - The response.

## AsyncMessageListenerMatches Objects

```python
class AsyncMessageListenerMatches(AsyncMiddleware)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

#### select\_consistent\_installation\_store

```python
def select_consistent_installation_store(
        client_id: str, app_store: Optional[AsyncInstallationStore],
        oauth_flow_store: Optional[AsyncInstallationStore],
        logger: Logger) -> Optional[AsyncInstallationStore]
```

#### get\_name\_for\_callable

```python
def get_name_for_callable(func: Callable) -> str
```

Returns the name for the given Callable function object.

**Arguments**:

- `func` - Either a `Callable` instance or a function, which as `__name__`
  

**Returns**:

  The name of the given Callable object

#### is\_callable\_coroutine

```python
def is_callable_coroutine(func: Optional[Any]) -> bool
```

## AsyncWorkflowStep Objects

```python
class AsyncWorkflowStep()
```

#### callback\_id

The Callback ID of the step from app

#### edit

`edit` listener, which displays a modal in Workflow Builder

#### save

`save` listener, which accepts workflow creator&#x27;s data submission in Workflow Builder

#### execute

`execute` listener, which processes the step from app execution

#### builder

```python
@classmethod
def builder(cls,
            callback_id: Union[str, Pattern],
            base_logger: Optional[Logger] = None) -> AsyncWorkflowStepBuilder
```

Deprecated:
    Steps from apps for legacy workflows are now deprecated.
    Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

#### build\_listener

```python
@classmethod
def build_listener(cls,
                   callback_id: Union[str, Pattern],
                   app_name: str,
                   listener_or_functions: Union[AsyncListener, Callable,
                                                List[Callable]],
                   name: str,
                   matchers: Optional[List[AsyncListenerMatcher]] = None,
                   middleware: Optional[List[AsyncMiddleware]] = None,
                   base_logger: Optional[Logger] = None)
```

## AsyncWorkflowStepBuilder Objects

```python
class AsyncWorkflowStepBuilder()
```

Steps from apps
Refer to https://docs.slack.dev/legacy/legacy-steps-from-apps/ for details.

#### callback\_id

#### edit

```python
def edit(*args,
         matchers: Optional[Union[Callable[..., Awaitable[bool]],
                                  AsyncListenerMatcher]] = None,
         middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
         lazy: Optional[List[Callable[..., Awaitable[None]]]] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new edit listener with details.

You can use this method as decorator as well.

```python
    @my_step.edit
    def edit_my_step(ack, configure):
        pass
```

It&#x27;s also possible to add additional listener matchers and/or middleware

```python
    @my_step.edit(matchers=[is_valid], middleware=[update_context])
    def edit_my_step(ack, configure):
        pass
```

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### save

```python
def save(*args,
         matchers: Optional[Union[Callable[..., Awaitable[bool]],
                                  AsyncListenerMatcher]] = None,
         middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
         lazy: Optional[List[Callable[..., Awaitable[None]]]] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new save listener with details.

You can use this method as decorator as well.

```python
    @my_step.save
    def save_my_step(ack, step, update):
        pass
```

It&#x27;s also possible to add additional listener matchers and/or middleware

```python
    @my_step.save(matchers=[is_valid], middleware=[update_context])
    def save_my_step(ack, step, update):
        pass
```

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### execute

```python
def execute(*args,
            matchers: Optional[Union[Callable[..., Awaitable[bool]],
                                     AsyncListenerMatcher]] = None,
            middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
            lazy: Optional[List[Callable[..., Awaitable[None]]]] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Registers a new execute listener with details.

You can use this method as decorator as well.

```python
    @my_step.execute
    def execute_my_step(step, complete, fail):
        pass
```

It&#x27;s also possible to add additional listener matchers and/or middleware

```python
    @my_step.save(matchers=[is_valid], middleware=[update_context])
    def execute_my_step(step, complete, fail):
        pass
```

For further information about AsyncWorkflowStep specific function arguments
such as `configure`, `update`, `complete`, and `fail`,
refer to the `async` prefixed ones in `slack_bolt.workflows.step.utilities` API documents.

**Arguments**:

- `*args` - This method can behave as either decorator or a method
- `matchers` - Listener matchers
- `middleware` - Listener middleware
- `lazy` - Lazy listeners

#### build

```python
def build(base_logger: Optional[Logger] = None) -> "AsyncWorkflowStep"
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

Constructs a WorkflowStep object. This method may raise an exception
if the builder doesn&#x27;t have enough configurations to build the object.

**Returns**:

  An `AsyncWorkflowStep` object

#### to\_listener\_matchers

```python
@staticmethod
def to_listener_matchers(
    app_name: str, matchers: Optional[List[Union[Callable[...,
                                                          Awaitable[bool]],
                                                 AsyncListenerMatcher]]]
) -> List[AsyncListenerMatcher]
```

#### to\_listener\_middleware

```python
@staticmethod
def to_listener_middleware(
    app_name: str, middleware: Optional[List[Union[Callable, AsyncMiddleware]]]
) -> List[AsyncMiddleware]
```

## AsyncWorkflowStepMiddleware Objects

```python
class AsyncWorkflowStepMiddleware(AsyncMiddleware)
```

Base middleware for step from app specific ones

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

## AuthorizeResult Objects

```python
class AuthorizeResult(dict)
```

Authorize function call result

#### enterprise\_id

#### team\_id

#### team

since v1.18

#### url

since v1.18

#### bot\_id

#### bot\_user\_id

#### bot\_token

#### bot\_scopes

since v1.17

#### user\_id

#### user

since v1.18

#### user\_token

#### user\_scopes

since v1.17

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

## AsyncAuthorize Objects

```python
class AsyncAuthorize()
```

This provides authorize function that returns AuthorizeResult
for an incoming request from Slack.

## AsyncCallableAuthorize Objects

```python
class AsyncCallableAuthorize(AsyncAuthorize)
```

When you pass the authorize argument in AsyncApp constructor,
This authorize implementation will be used.

## AsyncInstallationStoreAuthorize Objects

```python
class AsyncInstallationStoreAuthorize(AsyncAuthorize)
```

If you use the OAuth flow settings, this authorize implementation will be used.
As long as your own InstallationStore (or the built-in ones) works as you expect,
you can expect that the authorize layer should work for you without any customization.

#### authorize\_result\_cache

#### bot\_only

#### user\_token\_resolution

#### find\_installation\_available

#### find\_bot\_available

#### token\_rotator

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

## BoltUnhandledRequestError Objects

```python
class BoltUnhandledRequestError(BoltError)
```

#### request

type: ignore[name-defined]

#### body

#### current\_response

type: ignore[name-defined]

#### last\_global\_middleware\_name

#### error\_oauth\_flow\_or\_authorize\_required

```python
def error_oauth_flow_or_authorize_required() -> str
```

#### warning\_client\_prioritized\_and\_token\_skipped

```python
def warning_client_prioritized_and_token_skipped() -> str
```

#### warning\_token\_skipped

```python
def warning_token_skipped() -> str
```

#### error\_token\_required

```python
def error_token_required() -> str
```

#### warning\_unhandled\_request

```python
def warning_unhandled_request(
        req: Union[BoltRequest, "AsyncBoltRequest"]) -> str
```

#### debug\_checking\_listener

```python
def debug_checking_listener(listener_name: str) -> str
```

#### debug\_running\_listener

```python
def debug_running_listener(listener_name: str) -> str
```

#### error\_unexpected\_listener\_middleware

```python
def error_unexpected_listener_middleware(middleware_type) -> str
```

#### error\_listener\_function\_must\_be\_coro\_func

```python
def error_listener_function_must_be_coro_func(func_name: str) -> str
```

#### error\_client\_invalid\_type\_async

```python
def error_client_invalid_type_async() -> str
```

#### error\_authorize\_conflicts

```python
def error_authorize_conflicts() -> str
```

#### error\_oauth\_settings\_invalid\_type\_async

```python
def error_oauth_settings_invalid_type_async() -> str
```

#### error\_oauth\_flow\_invalid\_type\_async

```python
def error_oauth_flow_invalid_type_async() -> str
```

#### warning\_bot\_only\_conflicts

```python
def warning_bot_only_conflicts() -> str
```

#### debug\_return\_listener\_middleware\_response

```python
def debug_return_listener_middleware_response(listener_name: str, status: int,
                                              body: str,
                                              starting_time: float) -> str
```

#### info\_default\_oauth\_settings\_loaded

```python
def info_default_oauth_settings_loaded() -> str
```

#### error\_installation\_store\_required\_for\_builtin\_listeners

```python
def error_installation_store_required_for_builtin_listeners() -> str
```

#### warning\_unhandled\_by\_global\_middleware

```python
def warning_unhandled_by_global_middleware(
        name: str, req: Union[BoltRequest, "AsyncBoltRequest"]) -> str
```

#### warning\_ack\_timeout\_has\_no\_effect

```python
def warning_ack_timeout_has_no_effect(identifier: Union[str, Pattern],
                                      ack_timeout: int) -> str
```

## AsyncioLazyListenerRunner Objects

```python
class AsyncioLazyListenerRunner(AsyncLazyListenerRunner)
```

#### logger

#### start

```python
def start(function: Callable[..., Awaitable[None]],
          request: AsyncBoltRequest) -> None
```

## AsyncListener Objects

```python
class AsyncListener(metaclass=ABCMeta)
```

#### matchers

#### middleware

#### ack\_function

#### lazy\_functions

#### auto\_acknowledgement

#### ack\_timeout

#### async\_matches

```python
async def async_matches(*, req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

#### run\_async\_middleware

```python
async def run_async_middleware(
        *, req: AsyncBoltRequest,
        resp: BoltResponse) -> Tuple[Optional[BoltResponse], bool]
```

Runs an async middleware.

**Arguments**:

- `req` - The incoming request
- `resp` - The current response
  

**Returns**:

  A tuple of the processed response and a flag indicating termination

#### run\_ack\_function

```python
@abstractmethod
async def run_ack_function(*, request: AsyncBoltRequest,
                           response: BoltResponse) -> Optional[BoltResponse]
```

Runs all the registered middleware and then run the listener function.

**Arguments**:

- `request` - The incoming request
- `response` - The current response
  

**Returns**:

  The processed response

## AsyncCustomListener Objects

```python
class AsyncCustomListener(AsyncListener)
```

#### app\_name

#### ack\_function

type: ignore[assignment]

#### lazy\_functions

#### matchers

#### middleware

#### auto\_acknowledgement

#### ack\_timeout

#### arg\_names

#### logger

#### run\_ack\_function

```python
async def run_ack_function(*, request: AsyncBoltRequest,
                           response: BoltResponse) -> Optional[BoltResponse]
```

## AsyncDefaultListenerErrorHandler Objects

```python
class AsyncDefaultListenerErrorHandler(AsyncListenerErrorHandler)
```

#### handle

```python
async def handle(error: Exception, request: AsyncBoltRequest,
                 response: Optional[BoltResponse])
```

## AsyncCustomListenerErrorHandler Objects

```python
class AsyncCustomListenerErrorHandler(AsyncListenerErrorHandler)
```

#### handle

```python
async def handle(error: Exception, request: AsyncBoltRequest,
                 response: Optional[BoltResponse]) -> None
```

## AsyncListenerMatcher Objects

```python
class AsyncListenerMatcher(metaclass=ABCMeta)
```

#### async\_matches

```python
@abstractmethod
async def async_matches(req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` - The request
- `resp` - The response
  

**Returns**:

  True if matched

## AsyncCustomListenerMatcher Objects

```python
class AsyncCustomListenerMatcher(AsyncListenerMatcher)
```

#### app\_name

#### func

#### arg\_names

#### logger

#### async\_matches

```python
async def async_matches(req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

#### get\_bolt\_logger

```python
def get_bolt_logger(cls: Any, base_logger: Optional[Logger] = None) -> Logger
```

#### get\_bolt\_app\_logger

```python
def get_bolt_app_logger(app_name: str,
                        cls: object = None,
                        base_logger: Optional[Logger] = None) -> Logger
```

## AsyncSslCheck Objects

```python
class AsyncSslCheck(SslCheck, AsyncMiddleware)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

## AsyncRequestVerification Objects

```python
class AsyncRequestVerification(RequestVerification, AsyncMiddleware)
```

Verifies an incoming request by checking the validity of
`x-slack-signature`, `x-slack-request-timestamp`, and its body data.

Refer to https://docs.slack.dev/authentication/verifying-requests-from-slack/ for details.

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

## AsyncIgnoringSelfEvents Objects

```python
class AsyncIgnoringSelfEvents(IgnoringSelfEvents, AsyncMiddleware)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

## AsyncUrlVerification Objects

```python
class AsyncUrlVerification(UrlVerification, AsyncMiddleware)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

## AsyncAttachingFunctionToken Objects

```python
class AsyncAttachingFunctionToken(AsyncMiddleware)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

## AsyncAttachingConversationKwargs Objects

```python
class AsyncAttachingConversationKwargs(AsyncMiddleware)
```

#### thread\_context\_store

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

## AsyncMiddleware Objects

```python
class AsyncMiddleware(metaclass=ABCMeta)
```

A middleware can process request data before other middleware and listener functions.

#### async\_process

```python
@abstractmethod
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

```python
    @app.middleware
    async def simple_middleware(req, resp, next):
        # do something here
        await next()
```

This `async_process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
    @app.middleware
    async def simple_middleware(req, resp, next_):
        # do something here
        await next_()
```

**Arguments**:

- `req` - The incoming request
- `resp` - The response
- `next` - The function to tell the chain that it can continue
  

**Returns**:

  Processed response (optional)

#### name

```python
@property
def name() -> str
```

The name of this middleware

## AsyncCustomMiddleware Objects

```python
class AsyncCustomMiddleware(AsyncMiddleware)
```

#### app\_name

#### func

#### arg\_names

#### logger

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

#### name

```python
@property
def name() -> str
```

## AsyncMultiTeamsAuthorization Objects

```python
class AsyncMultiTeamsAuthorization(AsyncAuthorization)
```

#### authorize

#### user\_token\_resolution

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```

## AsyncSingleTeamAuthorization Objects

```python
class AsyncSingleTeamAuthorization(AsyncAuthorization)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
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

## AsyncOAuthSettings Objects

```python
class AsyncOAuthSettings()
```

#### client\_id

#### client\_secret

#### scopes

#### user\_scopes

#### redirect\_uri

#### install\_path

#### install\_page\_rendering\_enabled

#### redirect\_uri\_path

#### callback\_options

#### success\_url

#### failure\_url

#### authorization\_url

default: https://slack.com/oauth/v2/authorize

#### installation\_store

#### installation\_store\_bot\_only

#### token\_rotation\_expiration\_minutes

#### user\_token\_resolution

#### authorize

#### state\_validation\_enabled

#### state\_store

#### state\_cookie\_name

#### state\_expiration\_seconds

#### state\_utils

#### authorize\_url\_generator

#### redirect\_uri\_page\_renderer

#### logger

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

#### to\_copyable

```python
def to_copyable() -> "AsyncBoltRequest"
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

#### create\_async\_web\_client

```python
def create_async_web_client(token: Optional[str] = None,
                            logger: Optional[Logger] = None) -> AsyncWebClient
```

## AsyncApp Objects

```python
class AsyncApp()
```

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

