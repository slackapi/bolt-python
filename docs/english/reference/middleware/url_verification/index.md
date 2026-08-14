---
sidebar_label: url_verification
title: slack_bolt.middleware.url_verification
---

## UrlVerification Objects

```python
class UrlVerification(Middleware)
```

#### \_\_init\_\_

```python
def __init__(base_logger: Optional[Logger] = None)
```

Handles url_verification requests.

Refer to https://docs.slack.dev/reference/events/url_verification/ for details.

**Arguments**:

- `base_logger` - The base logger

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

