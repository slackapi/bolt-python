---
sidebar_label: async_listener_matcher
title: slack_bolt.listener_matcher.async_listener_matcher
---

## AsyncListenerMatcher Objects

```python
class AsyncListenerMatcher()
```

#### async\_matches

```python
async def async_matches(req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` _AsyncBoltRequest_ - The request
- `resp` _BoltResponse_ - The response

**Returns**:

- `bool` - True if matched

## AsyncCustomListenerMatcher Objects

```python
class AsyncCustomListenerMatcher(AsyncListenerMatcher)
```

#### app\_name: `str`

#### func: `Callable[..., Awaitable[bool]]`

#### arg\_names: `Sequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(
    *,
    app_name: str,
    func: Callable[..., Awaitable[bool]],
    base_logger: Optional[Logger] = None)
```

#### async\_matches

```python
async def async_matches(req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

#### builtin\_async\_listener\_matcher\_classes
