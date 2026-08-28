---
sidebar_label: listener_matcher
title: slack_bolt.listener_matcher
---

A listener matcher is a simplified version of listener middleware.

A listener matcher function returns bool value instead of `next()` method invocation inside.
This interface enables developers to utilize simple predicate functions for additional listener conditions.

## `ListenerMatcher`

### `matches`

```python
matches(req, resp)
```

Matches against the request and returns True if matched.

**Parameters:**

- **req** (BoltRequest) – The request
- **resp** (BoltResponse) – The response

**Returns:**

- bool – True if matched.

## Submodules

- [slack_bolt.listener_matcher.async_builtins](/tools/bolt-python/reference/listener_matcher/async_builtins)
- [slack_bolt.listener_matcher.async_listener_matcher](/tools/bolt-python/reference/listener_matcher/async_listener_matcher)
- [slack_bolt.listener_matcher.builtins](/tools/bolt-python/reference/listener_matcher/builtins)
- [slack_bolt.listener_matcher.custom_listener_matcher](/tools/bolt-python/reference/listener_matcher/custom_listener_matcher)
- [slack_bolt.listener_matcher.listener_matcher](/tools/bolt-python/reference/listener_matcher/listener_matcher)
