---
sidebar_label: ssl_check
title: slack_bolt.middleware.ssl_check
---

## Submodules

- [slack_bolt.middleware.ssl_check.async_ssl_check](/tools/bolt-python/reference/middleware/ssl_check/async_ssl_check)
- [slack_bolt.middleware.ssl_check.ssl_check](/tools/bolt-python/reference/middleware/ssl_check/ssl_check)

## SslCheck Objects

```python
class SslCheck(Middleware)
```

#### verification\_token

The verification token to check (optional as it&#x27;s already deprecated -
https://docs.slack.dev/authentication/verifying-requests-from-slack/`deprecation`)

#### logger

#### \_\_init\_\_

```python
def __init__(verification_token: Optional[str] = None,
             base_logger: Optional[Logger] = None)
```

Handles `ssl_check` requests.
Refer to https://docs.slack.dev/interactivity/implementing-slash-commands/ for details.

**Arguments**:

- `verification_token` - The verification token to check
  (optional as it&#x27;s already deprecated - https://docs.slack.dev/authentication/verifying-requests-from-slack/`deprecation`)
- `base_logger` - The base logger

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

