---
sidebar_label: async_internals
title: slack_bolt.lazy_listener.async_internals
---

#### build\_async\_required\_kwargs

```python
def build_async_required_kwargs(
        *,
        logger: logging.Logger,
        required_arg_names: MutableSequence[str],
        request: AsyncBoltRequest,
        response: Optional[BoltResponse],
        next_func: Optional[Callable[[], None]] = None,
        this_func: Optional[Callable] = None,
        error: Optional[Exception] = None,
        next_keys_required: bool = True) -> Dict[str, Any]
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

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
```

#### to\_runnable\_function

```python
async def to_runnable_function(internal_func: Callable[..., Awaitable[None]],
                               logger: Logger, request: AsyncBoltRequest)
```

