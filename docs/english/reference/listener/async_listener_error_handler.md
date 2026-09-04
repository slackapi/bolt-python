---
sidebar_label: async_listener_error_handler
title: slack_bolt.listener.async_listener_error_handler
---

## `AsyncListenerErrorHandler`

### `handle`

```python
handle(error, request, response)
```

Handles an unhandled exception.

**Parameters:**

- **error** (Exception) – The raised exception.
- **request** (AsyncBoltRequest) – The request.
- **response** (Optional[BoltResponse]) – The response.
