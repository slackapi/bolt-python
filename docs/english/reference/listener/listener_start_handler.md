---
sidebar_label: listener_start_handler
title: slack_bolt.listener.listener_start_handler
---

## `ListenerStartHandler`

### `handle`

```python
handle(request, response)
```

Do something extra before the listener execution.

This handler is useful if a developer needs to maintain/clean up
thread-local resources such as Django ORM database connections
before a listener execution starts.

**Parameters:**

- **request** (BoltRequest) – The request.
- **response** (Optional[BoltResponse]) – The response.
