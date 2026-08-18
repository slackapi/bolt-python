---
sidebar_label: async_assistant
title: slack_bolt.middleware.assistant.async_assistant
---

## AsyncSaveThreadContext Objects

```python
class AsyncSaveThreadContext()
```

#### thread\_context\_store: `AsyncAssistantThreadContextStore`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AsyncAssistantThreadContextStore,
             channel_id: str, thread_ts: str)
```

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

## AsyncioListenerRunner Objects

```python
class AsyncioListenerRunner()
```

#### logger: `Logger`

#### process\_before\_response: `bool`

#### listener\_error\_handler: `AsyncListenerErrorHandler`

#### listener\_start\_handler: `AsyncListenerStartHandler`

#### listener\_completion\_handler: `AsyncListenerCompletionHandler`

#### lazy\_listener\_runner: `AsyncLazyListenerRunner`

#### \_\_init\_\_

```python
def __init__(logger: Logger, process_before_response: bool,
             listener_error_handler: AsyncListenerErrorHandler,
             listener_start_handler: AsyncListenerStartHandler,
             listener_completion_handler: AsyncListenerCompletionHandler,
             lazy_listener_runner: AsyncLazyListenerRunner)
```

#### run

```python
async def run(request: AsyncBoltRequest,
              response: BoltResponse,
              listener_name: str,
              listener: AsyncListener,
              starting_time: Optional[float] = None) -> Optional[BoltResponse]
```

#### build\_listener\_matcher

```python
def build_listener_matcher(
    func: Callable[..., bool],
    asyncio: bool,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

## AsyncAttachingConversationKwargs Objects

```python
class AsyncAttachingConversationKwargs(AsyncMiddleware)
```

#### thread\_context\_store: `Optional[AsyncAssistantThreadContextStore]`

#### \_\_init\_\_

```python
def __init__(
        thread_context_store: Optional[AsyncAssistantThreadContextStore] = None
)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body: `str`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### context: `AsyncBoltContext`

The context in this request.

#### lazy\_only: `bool`

#### lazy\_function\_name: `Optional[str]`

#### mode: `str`

The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

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

## BoltResponse Objects

```python
class BoltResponse()
```

#### status: `int`

HTTP status code

#### body: `str`

The response body (dict and str are supported)

#### headers: `Dict[str, Sequence[str]]`

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

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

## AsyncListener Objects

```python
class AsyncListener(metaclass=ABCMeta)
```

#### matchers: `Sequence[AsyncListenerMatcher]`

#### middleware: `Sequence[AsyncMiddleware]`

#### ack\_function: `Callable[..., Awaitable[BoltResponse]]`

#### lazy\_functions: `Sequence[Callable[..., Awaitable[None]]]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

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

#### app\_name: `str`

#### ack\_function: `Callable[..., Awaitable[Optional[BoltResponse]]]`

type: ignore[assignment]

#### lazy\_functions: `Sequence[Callable[..., Awaitable[None]]]`

#### matchers: `Sequence[AsyncListenerMatcher]`

#### middleware: `Sequence[AsyncMiddleware]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             ack_function: Callable[..., Awaitable[Optional[BoltResponse]]],
             lazy_functions: Sequence[Callable[..., Awaitable[None]]],
             matchers: Sequence[AsyncListenerMatcher],
             middleware: Sequence[AsyncMiddleware],
             auto_acknowledgement: bool = False,
             ack_timeout: int = 3,
             base_logger: Optional[Logger] = None)
```

#### run\_ack\_function

```python
async def run_ack_function(*, request: AsyncBoltRequest,
                           response: BoltResponse) -> Optional[BoltResponse]
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

#### is\_assistant\_thread\_started\_event

```python
def is_assistant_thread_started_event(body: Dict[str, Any]) -> bool
```

#### is\_user\_message\_event\_in\_assistant\_thread

```python
def is_user_message_event_in_assistant_thread(body: Dict[str, Any]) -> bool
```

#### is\_assistant\_thread\_context\_changed\_event

```python
def is_assistant_thread_context_changed_event(body: Dict[str, Any]) -> bool
```

#### is\_other\_message\_sub\_event\_in\_assistant\_thread

```python
def is_other_message_sub_event_in_assistant_thread(
        body: Dict[str, Any]) -> bool
```

#### is\_bot\_message\_event\_in\_assistant\_thread

```python
def is_bot_message_event_in_assistant_thread(body: Dict[str, Any]) -> bool
```

#### is\_used\_without\_argument

```python
def is_used_without_argument(args) -> bool
```

Tests if a decorator invocation is without () or (args).

**Arguments**:

- `args` - arguments
  

**Returns**:

  True if it&#x27;s an invocation without args

## AsyncAssistant Objects

```python
class AsyncAssistant(AsyncMiddleware)
```

#### thread\_context\_store: `Optional[AsyncAssistantThreadContextStore]`

#### base\_logger: `Optional[logging.Logger]`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str = "assistant",
             thread_context_store: Optional[
                 AsyncAssistantThreadContextStore] = None,
             logger: Optional[logging.Logger] = None)
```

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

