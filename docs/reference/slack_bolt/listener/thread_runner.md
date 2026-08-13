---
sidebar_label: thread_runner
title: slack_bolt.listener.thread_runner
---

## LazyListenerRunner Objects

```python
class LazyListenerRunner(metaclass=ABCMeta)
```

#### logger

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

#### logger

#### process\_before\_response

#### listener\_error\_handler

#### listener\_start\_handler

#### listener\_completion\_handler

#### listener\_executor

#### lazy\_listener\_runner

#### run

```python
def run(request: BoltRequest,
        response: BoltResponse,
        listener_name: str,
        listener: Listener,
        starting_time: Optional[float] = None) -> Optional[BoltResponse]
```

