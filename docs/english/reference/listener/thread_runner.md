---
sidebar_label: thread_runner
title: slack_bolt.listener.thread_runner
---

## LazyListenerRunner Objects

```python
class LazyListenerRunner(metaclass=ABCMeta)
```

#### logger: `Logger`

#### start

```python
@abstractmethod
def start(function: Callable[..., None], request: BoltRequest) -> None
```

Starts a new lazy listener execution.

**Arguments**:

- `function` - The function to run.
- `request` - The request to pass to the function. The object must be thread-safe.

#### run

```python
def run(function: Callable[..., None], request: BoltRequest) -> None
```

Synchronously runs the function with a given request data.

**Arguments**:

- `function` - The function to run.
- `request` - The request to pass to the function. The object must be thread-safe.

## Listener Objects

```python
class Listener(metaclass=ABCMeta)
```

#### matchers: `Sequence[ListenerMatcher]`

#### middleware: `Sequence[Middleware]`

#### ack\_function: `Callable[..., BoltResponse]`

#### lazy\_functions: `Sequence[Callable[..., None]]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

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

## ListenerStartHandler Objects

```python
class ListenerStartHandler(metaclass=ABCMeta)
```

#### handle

```python
@abstractmethod
def handle(request: BoltRequest, response: Optional[BoltResponse]) -> None
```

Do something extra before the listener execution.

This handler is useful if a developer needs to maintain/clean up
thread-local resources such as Django ORM database connections
before a listener execution starts.

**Arguments**:

- `request` - The request.
- `response` - The response.

## ListenerCompletionHandler Objects

```python
class ListenerCompletionHandler(metaclass=ABCMeta)
```

#### handle

```python
@abstractmethod
def handle(request: BoltRequest, response: Optional[BoltResponse]) -> None
```

Do something extra after the listener execution

**Arguments**:

- `request` - The request.
- `response` - The response.

## ListenerErrorHandler Objects

```python
class ListenerErrorHandler(metaclass=ABCMeta)
```

#### handle

```python
@abstractmethod
def handle(error: Exception, request: BoltRequest,
           response: Optional[BoltResponse]) -> None
```

Handles an unhandled exception.

**Arguments**:

- `error` - The raised exception.
- `request` - The request.
- `response` - The response.

#### debug\_responding

```python
def debug_responding(status: int, body: str, millis: int) -> str
```

#### debug\_running\_lazy\_listener

```python
def debug_running_lazy_listener(func_name: str) -> str
```

#### warning\_did\_not\_call\_ack

```python
def warning_did_not_call_ack(listener_name: str) -> str
```

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body: `str`

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### context: `BoltContext`

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
def to_copyable() -> "BoltRequest"
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

#### create\_copy

```python
def create_copy(original: Any) -> Any
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

## ThreadListenerRunner Objects

```python
class ThreadListenerRunner()
```

#### logger: `Logger`

#### process\_before\_response: `bool`

#### listener\_error\_handler: `ListenerErrorHandler`

#### listener\_start\_handler: `ListenerStartHandler`

#### listener\_completion\_handler: `ListenerCompletionHandler`

#### listener\_executor: `Executor`

#### lazy\_listener\_runner: `LazyListenerRunner`

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

