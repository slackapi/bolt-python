---
sidebar_label: listener
title: slack_bolt.listener.listener
slug: listener
---

## `Listener`

### `run_ack_function`

```python
run_ack_function(*, request, response)
```

Runs all the registered middleware and then run the listener function.

**Parameters:**

- **request** (BoltRequest) – The incoming request
- **response** (BoltResponse) – The current response

**Returns:**

- Optional[BoltResponse] – The processed response

### `run_middleware`

```python
run_middleware(*, req, resp)
```

Runs a middleware.

**Parameters:**

- **req** (BoltRequest) – The incoming request
- **resp** (BoltResponse) – The current response

**Returns:**

- Tuple[Optional[BoltResponse], bool] – A tuple of the processed response and a flag indicating termination
