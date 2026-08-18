---
sidebar_label: asyncio_runner
title: slack_bolt.listener.asyncio_runner
---

## AsyncAck Objects

```python
class AsyncAck()
```

#### response

#### \_\_init\_\_

```python
def __init__()
```

## AsyncLazyListenerRunner Objects

```python
class AsyncLazyListenerRunner(metaclass=ABCMeta)
```

#### logger

#### start

```python
@abstractmethod
def start(function: Callable[..., Awaitable[None]],
          request: AsyncBoltRequest) -> None
```

Starts a new lazy listener execution.

**Arguments**:

- `function` - The function to run.
- `request` - The request to pass to the function. The object must be thread-safe.

#### run

```python
async def run(function: Callable[..., Awaitable[None]],
              request: AsyncBoltRequest) -> None
```

Synchronously run the function with a given request data.

**Arguments**:

- `function` - The function to run.
- `request` - The request to pass to the function. The object must be thread-safe.

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

## AsyncListenerStartHandler Objects

```python
class AsyncListenerStartHandler(metaclass=ABCMeta)
```

#### handle

```python
@abstractmethod
async def handle(request: AsyncBoltRequest,
                 response: Optional[BoltResponse]) -> None
```

Do something extra before the listener execution

**Arguments**:

- `request` - The request.
- `response` - The response.

## AsyncListenerCompletionHandler Objects

```python
class AsyncListenerCompletionHandler(metaclass=ABCMeta)
```

#### handle

```python
@abstractmethod
async def handle(request: AsyncBoltRequest,
                 response: Optional[BoltResponse]) -> None
```

Do something extra after the listener execution

**Arguments**:

- `request` - The request.
- `response` - The response.

## AsyncListenerErrorHandler Objects

```python
class AsyncListenerErrorHandler(metaclass=ABCMeta)
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

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body

#### body

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### query

The query string data in any data format.

#### headers

The request headers.

#### content\_type

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
def to_copyable() -> "AsyncBoltRequest"
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

