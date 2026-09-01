---
sidebar_label: async_listener
title: slack_bolt.listener.async_listener
---

## `AsyncListener`

### `run_ack_function`

```python
run_ack_function(*, request, response)
```

Runs all the registered middleware and then run the listener function.

**Parameters:**

- **request** (AsyncBoltRequest) – The incoming request
- **response** (BoltResponse) – The current response

**Returns:**

- Optional[BoltResponse] – The processed response

### `run_async_middleware`

```python
run_async_middleware(*, req, resp)
```

Runs an async middleware.

**Parameters:**

- **req** (AsyncBoltRequest) – The incoming request
- **resp** (BoltResponse) – The current response

**Returns:**

- Tuple[Optional[BoltResponse], bool] – A tuple of the processed response and a flag indicating termination
