---
sidebar_label: request_verification
title: slack_bolt.middleware.request_verification.request_verification
slug: request_verification
---

## RequestVerification Objects

```python
class RequestVerification(Middleware)
```

#### \_\_init\_\_

```python
def __init__(signing_secret: str, base_logger: Optional[Logger] = None)
```

Verifies an incoming request from Slack.

Checks the validity of `x-slack-signature`, `x-slack-request-timestamp`, and the request body data.

Refer to https://docs.slack.dev/authentication/verifying-requests-from-slack/ for details.

**Arguments**:

- `signing_secret` _str_ - The signing secret
- `base_logger` _Optional[Logger]_ - The base logger

#### verifier

```python
@property
def verifier() -> SignatureVerifier
```

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> BoltResponse
```
