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

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
```

#### to\_runnable\_function

```python
async def to_runnable_function(internal_func: Callable[..., Awaitable[None]],
                               logger: Logger, request: AsyncBoltRequest)
```

