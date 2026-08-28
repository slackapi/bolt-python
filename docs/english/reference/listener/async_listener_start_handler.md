---
sidebar_label: async_listener_start_handler
title: slack_bolt.listener.async_listener_start_handler
---

## AsyncListenerStartHandler Objects

```python
class AsyncListenerStartHandler()
```

#### handle

```python
async def handle(request: AsyncBoltRequest, response: Optional[BoltResponse]) -> None
```

Do something extra before the listener execution.

**Arguments**:

- `request` _AsyncBoltRequest_ - The request.
- `response` _Optional[BoltResponse]_ - The response.

## AsyncCustomListenerStartHandler Objects

```python
class AsyncCustomListenerStartHandler(AsyncListenerStartHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, func: Callable[..., Awaitable[None]])
```

#### handle

```python
async def handle(request: AsyncBoltRequest, response: Optional[BoltResponse]) -> None
```

## AsyncDefaultListenerStartHandler Objects

```python
class AsyncDefaultListenerStartHandler(AsyncListenerStartHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### handle

```python
async def handle(request: AsyncBoltRequest, response: Optional[BoltResponse])
```
