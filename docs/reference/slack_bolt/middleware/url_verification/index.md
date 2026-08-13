---
sidebar_label: url_verification
title: slack_bolt.middleware.url_verification
---

## UrlVerification Objects

```python
class UrlVerification(Middleware)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

