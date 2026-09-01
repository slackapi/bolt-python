---
sidebar_label: middleware_error_handler
title: slack_bolt.middleware.middleware_error_handler
---

## `MiddlewareErrorHandler`

### `handle`

```python
handle(error, request, response)
```

Handles an unhandled exception.

**Parameters:**

- **error** (Exception) – The raised exception.
- **request** (BoltRequest) – The request.
- **response** (Optional[BoltResponse]) – The response.
