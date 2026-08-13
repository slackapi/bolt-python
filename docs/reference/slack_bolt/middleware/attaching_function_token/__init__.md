---
sidebar_label: attaching_function_token
title: slack_bolt.middleware.attaching_function_token
---

## AttachingFunctionToken Objects

```python
class AttachingFunctionToken(Middleware)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

