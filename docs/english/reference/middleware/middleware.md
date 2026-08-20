---
sidebar_label: middleware
title: slack_bolt.middleware.middleware
slug: middleware
---

## Middleware Objects

```python
class Middleware()
```

A middleware can process request data before other middleware and listener functions.

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

    @app.middleware
    def simple_middleware(req, resp, next):
        # do something here
        next()

This `process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

    @app.middleware
    def simple_middleware(req, resp, next_):
        # do something here
        next_()

**Arguments**:

- `req` _BoltRequest_ - The incoming request
- `resp` _BoltResponse_ - The response
- `next` _Callable[[], BoltResponse]_ - The function to tell the chain that it can continue

**Returns**:

- `Optional[BoltResponse]` - Processed response (optional)

#### name

```python
@property
def name() -> str
```

The name of this middleware
