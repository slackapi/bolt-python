---
sidebar_label: assistant
title: slack_bolt.middleware.assistant.assistant
slug: assistant
---

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

#### build\_listener\_matcher

```python
def build_listener_matcher(
    func: Callable[..., bool],
    asyncio: bool,
    base_logger: Optional[Logger] = None
) -> Union[ListenerMatcher, "AsyncListenerMatcher"]
```

## AttachingConversationKwargs Objects

```python
class AttachingConversationKwargs(Middleware)
```

#### thread\_context\_store

#### \_\_init\_\_

```python
def __init__(
        thread_context_store: Optional[AssistantThreadContextStore] = None)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body

#### query

The query string data in any data format.

#### headers

The request headers.

#### content\_type

#### body

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### context

The context in this request.

#### lazy\_only

#### lazy\_function\_name

#### mode

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
def to_copyable() -> "BoltRequest"
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

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

## CustomListener Objects

```python
class CustomListener(Listener)
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

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             ack_function: Callable[..., Optional[BoltResponse]],
             lazy_functions: Sequence[Callable[..., None]],
             matchers: Sequence[ListenerMatcher],
             middleware: Sequence[Middleware],
             auto_acknowledgement: bool = False,
             ack_timeout: int = 3,
             base_logger: Optional[Logger] = None)
```

#### run\_ack\_function

```python
def run_ack_function(*, request: BoltRequest,
                     response: BoltResponse) -> Optional[BoltResponse]
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

## ThreadListenerRunner Objects

```python
class ThreadListenerRunner()
```

#### logger

#### process\_before\_response

#### listener\_error\_handler

#### listener\_start\_handler

#### listener\_completion\_handler

#### listener\_executor

#### lazy\_listener\_runner

#### \_\_init\_\_

```python
def __init__(logger: Logger, process_before_response: bool,
             listener_error_handler: ListenerErrorHandler,
             listener_start_handler: ListenerStartHandler,
             listener_completion_handler: ListenerCompletionHandler,
             listener_executor: Executor,
             lazy_listener_runner: LazyListenerRunner)
```

#### run

```python
def run(request: BoltRequest,
        response: BoltResponse,
        listener_name: str,
        listener: Listener,
        starting_time: Optional[float] = None) -> Optional[BoltResponse]
```

## Middleware Objects

```python
class Middleware(metaclass=ABCMeta)
```

A middleware can process request data before other middleware and listener functions.

#### process

```python
@abstractmethod
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

```python
    @app.middleware
    def simple_middleware(req, resp, next):
        # do something here
        next()
```

This `process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
    @app.middleware
    def simple_middleware(req, resp, next_):
        # do something here
        next_()
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

## ListenerMatcher Objects

```python
class ListenerMatcher(metaclass=ABCMeta)
```

#### matches

```python
@abstractmethod
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` - The request
- `resp` - The response
  

**Returns**:

  True if matched.

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

