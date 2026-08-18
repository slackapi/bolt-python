---
sidebar_label: asyncio_runner
title: slack_bolt.lazy_listener.asyncio_runner
---

#### to\_runnable\_function

```python
async def to_runnable_function(internal_func: Callable[..., Awaitable[None]],
                               logger: Logger, request: AsyncBoltRequest)
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

## AsyncioLazyListenerRunner Objects

```python
class AsyncioLazyListenerRunner(AsyncLazyListenerRunner)
```

#### logger

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### start

```python
def start(function: Callable[..., Awaitable[None]],
          request: AsyncBoltRequest) -> None
```

