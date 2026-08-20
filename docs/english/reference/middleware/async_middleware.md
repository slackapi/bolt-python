---
sidebar_label: async_middleware
title: slack_bolt.middleware.async_middleware
---

## AsyncMiddleware Objects

```python
class AsyncMiddleware()
```

A middleware can process request data before other middleware and listener functions.

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

    @app.middleware
    async def simple_middleware(req, resp, next):
        # do something here
        await next()

This `async_process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

    @app.middleware
    async def simple_middleware(req, resp, next_):
        # do something here
        await next_()

**Arguments**:

- `req` _AsyncBoltRequest_ - The incoming request
- `resp` _BoltResponse_ - The response
- `next` _Callable[[], Awaitable[BoltResponse]]_ - The function to tell the chain that it can continue

**Returns**:

- `Optional[BoltResponse]` - Processed response (optional)

#### name

```python
@property
def name() -> str
```

The name of this middleware
