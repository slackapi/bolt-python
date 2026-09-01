---
sidebar_label: async_middleware_error_handler
title: slack_bolt.middleware.async_middleware_error_handler
---

## `AsyncMiddlewareErrorHandler`

### `handle`

```python
handle(error, request, response)
```

Handles an unhandled exception.

**Parameters:**

- **error** (Exception) – The raised exception.
- **request** (AsyncBoltRequest) – The request.
- **response** (Optional[BoltResponse]) – The response.
