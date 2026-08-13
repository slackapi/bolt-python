---
sidebar_label: ssl_check
title: slack_bolt.middleware.ssl_check
---

## SslCheck Objects

```python
class SslCheck(Middleware)
```

#### verification\_token

#### logger

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

