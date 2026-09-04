---
sidebar_label: middleware
title: slack_bolt.middleware.middleware
slug: middleware
---

## `Middleware`

A middleware can process request data before other middleware and listener functions.

### `name`

```python
name: str
```

The name of this middleware.

### `process`

```python
process(*, req, resp, next)
```

Processes a request data before other middleware and listeners.

A middleware calls `next()` function if the chain should continue.

```python
@app.middleware
def simple_middleware(req, resp, next):
    # do something here
    next()
```

This `process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
@app.middleware
def simple_middleware(req, resp, next_):
    # do something here
    next_()
```

**Parameters:**

- **req** (BoltRequest) – The incoming request
- **resp** (BoltResponse) – The response
- **next** (Callable[[], BoltResponse]) – The function to tell the chain that it can continue

**Returns:**

- Optional[BoltResponse] – Processed response (optional)
