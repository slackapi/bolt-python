---
sidebar_label: listener_error_handler
title: slack_bolt.listener.listener_error_handler
---

## `ListenerErrorHandler`

### `handle`

```python
handle(error, request, response)
```

Handles an unhandled exception.

**Parameters:**

- **error** (Exception) – The raised exception.
- **request** (BoltRequest) – The request.
- **response** (Optional[BoltResponse]) – The response.
