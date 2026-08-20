---
sidebar_label: internals
title: slack_bolt.lazy_listener.internals
---

#### build\_runnable\_function

```python
def build_runnable_function(
    func: Callable[..., None],
    logger: Logger,
    request: BoltRequest) -> Callable[[], None]
```
