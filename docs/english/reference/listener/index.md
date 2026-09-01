---
sidebar_label: listener
title: slack_bolt.listener
---

Listeners process incoming requests from Slack.

A listener runs when the request's type or data structure matches its predefined conditions.
Typically, a listener acknowledges the request, processes its data, and may send a response back to Slack.

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

## Submodules

- [slack_bolt.listener.async_builtins](/tools/bolt-python/reference/listener/async_builtins)
- [slack_bolt.listener.async_listener](/tools/bolt-python/reference/listener/async_listener)
- [slack_bolt.listener.async_listener_completion_handler](/tools/bolt-python/reference/listener/async_listener_completion_handler)
- [slack_bolt.listener.async_listener_error_handler](/tools/bolt-python/reference/listener/async_listener_error_handler)
- [slack_bolt.listener.async_listener_start_handler](/tools/bolt-python/reference/listener/async_listener_start_handler)
- [slack_bolt.listener.asyncio_runner](/tools/bolt-python/reference/listener/asyncio_runner)
- [slack_bolt.listener.builtins](/tools/bolt-python/reference/listener/builtins)
- [slack_bolt.listener.custom_listener](/tools/bolt-python/reference/listener/custom_listener)
- [slack_bolt.listener.listener](/tools/bolt-python/reference/listener/listener)
- [slack_bolt.listener.listener_completion_handler](/tools/bolt-python/reference/listener/listener_completion_handler)
- [slack_bolt.listener.listener_error_handler](/tools/bolt-python/reference/listener/listener_error_handler)
- [slack_bolt.listener.listener_start_handler](/tools/bolt-python/reference/listener/listener_start_handler)
- [slack_bolt.listener.thread_runner](/tools/bolt-python/reference/listener/thread_runner)
