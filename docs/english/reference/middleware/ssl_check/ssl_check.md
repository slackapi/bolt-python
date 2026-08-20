---
sidebar_label: ssl_check
title: slack_bolt.middleware.ssl_check.ssl_check
slug: ssl_check
---

## SslCheck Objects

```python
class SslCheck(Middleware)
```

#### verification\_token: `Optional[str]`

The verification token to check (optional as it's already deprecated -
https://docs.slack.dev/authentication/verifying-requests-from-slack/#deprecation)

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(
    verification_token: Optional[str] = None,
    base_logger: Optional[Logger] = None)
```

Handles `ssl_check` requests.
Refer to https://docs.slack.dev/interactivity/implementing-slash-commands/ for details.

**Arguments**:

- `verification_token` _Optional[str]_ - The verification token to check
  (optional as it's already deprecated - https://docs.slack.dev/authentication/verifying-requests-from-slack/#deprecation)
- `base_logger` _Optional[Logger]_ - The base logger

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> BoltResponse
```
