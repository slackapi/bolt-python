---
sidebar_label: async_listener_matcher
title: slack_bolt.listener_matcher.async_listener_matcher
---

## `AsyncListenerMatcher`

### `async_matches`

```python
async_matches(req, resp)
```

Matches against the request and returns True if matched.

**Parameters:**

- **req** (AsyncBoltRequest) – The request
- **resp** (BoltResponse) – The response

**Returns:**

- bool – True if matched
