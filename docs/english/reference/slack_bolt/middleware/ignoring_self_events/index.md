---
sidebar_label: ignoring_self_events
title: slack_bolt.middleware.ignoring_self_events
---

## IgnoringSelfEvents Objects

```python
class IgnoringSelfEvents(Middleware)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

#### events\_that\_should\_be\_kept

