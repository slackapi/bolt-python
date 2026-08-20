---
sidebar_label: listener
title: slack_bolt.listener
---

## Submodules

- [slack_bolt.listener.async_builtins](/tools/bolt-python/reference/listener/async_builtins)
- [slack_bolt.listener.async_listener](/tools/bolt-python/reference/listener/async_listener)
- [slack_bolt.listener.async_listener_completion_handler](/tools/bolt-python/reference/listener/async_listener_completion_handler)
- [slack_bolt.listener.async_listener_error_handler](/tools/bolt-python/reference/listener/async_listener_error_handler)
- [slack_bolt.listener.async_listener_start_handler](/tools/bolt-python/reference/listener/async_listener_start_handler)
- [slack_bolt.listener.asyncio_runner](/tools/bolt-python/reference/listener/asyncio_runner)
- [slack_bolt.listener.builtins](/tools/bolt-python/reference/listener/builtins)
- [slack_bolt.listener.custom_listener](/tools/bolt-python/reference/listener/custom_listener)
- [slack_bolt.listener.listener](/tools/bolt-python/reference/listener/listener)
- [slack_bolt.listener.listener_completion_handler](/tools/bolt-python/reference/listener/listener_completion_handler)
- [slack_bolt.listener.listener_error_handler](/tools/bolt-python/reference/listener/listener_error_handler)
- [slack_bolt.listener.listener_start_handler](/tools/bolt-python/reference/listener/listener_start_handler)
- [slack_bolt.listener.thread_runner](/tools/bolt-python/reference/listener/thread_runner)

## CustomListener Objects

```python
class CustomListener(Listener)
```

#### app\_name: `str`

#### ack\_function: `Callable[..., Optional[BoltResponse]]`

#### lazy\_functions: `Sequence[Callable[..., None]]`

#### matchers: `Sequence[ListenerMatcher]`

#### middleware: `Sequence[Middleware]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(
    *,
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
def run_ack_function(
    *,
    request: BoltRequest,
    response: BoltResponse) -> Optional[BoltResponse]
```

## Listener Objects

```python
class Listener()
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
def run_middleware(
    *,
    req: BoltRequest,
    resp: BoltResponse) -> Tuple[Optional[BoltResponse], bool]
```

Runs a middleware.

**Arguments**:

- `req` _BoltRequest_ - The incoming request
- `resp` _BoltResponse_ - The current response

**Returns**:

- `Tuple[Optional[BoltResponse], bool]` - A tuple of the processed response and a flag indicating termination

#### run\_ack\_function

```python
def run_ack_function(
    *,
    request: BoltRequest,
    response: BoltResponse) -> Optional[BoltResponse]
```

Runs all the registered middleware and then run the listener function.

**Arguments**:

- `request` _BoltRequest_ - The incoming request
- `response` _BoltResponse_ - The current response

**Returns**:

- `Optional[BoltResponse]` - The processed response

#### builtin\_listener\_classes
