---
sidebar_label: async_middleware
title: slack_bolt.middleware.async_middleware
---

## `AsyncMiddleware`

A middleware can process request data before other middleware and listener functions.

### `async_process`

```python
async_process(*, req, resp, next)
```

Processes a request data before other middleware and listeners.

A middleware calls `next()` function if the chain should continue.

```python
@app.middleware
async def simple_middleware(req, resp, next):
    # do something here
    await next()
```

This `async_process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
@app.middleware
async def simple_middleware(req, resp, next_):
    # do something here
    await next_()
```

**Parameters:**

- **req** (AsyncBoltRequest) – The incoming request
- **resp** (BoltResponse) – The response
- **next** (Callable[[], Awaitable[BoltResponse]]) – The function to tell the chain that it can continue

**Returns:**

- Optional[BoltResponse] – Processed response (optional)

### `name`

```python
name: str
```

The name of this middleware.
