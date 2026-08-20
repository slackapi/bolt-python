---
sidebar_label: listener_matcher
title: slack_bolt.listener_matcher.listener_matcher
slug: listener_matcher
---

## ListenerMatcher Objects

```python
class ListenerMatcher()
```

#### matches

```python
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` _BoltRequest_ - The request
- `resp` _BoltResponse_ - The response

**Returns**:

- `bool` - True if matched.
