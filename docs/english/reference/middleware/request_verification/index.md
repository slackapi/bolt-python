---
sidebar_label: request_verification
title: slack_bolt.middleware.request_verification
---

## Submodules

- [slack_bolt.middleware.request_verification.async_request_verification](/tools/bolt-python/reference/middleware/request_verification/async_request_verification)
- [slack_bolt.middleware.request_verification.request_verification](/tools/bolt-python/reference/middleware/request_verification/request_verification)

## RequestVerification Objects

```python
class RequestVerification(Middleware)
```

#### \_\_init\_\_

```python
def __init__(signing_secret: str, base_logger: Optional[Logger] = None)
```

Verifies an incoming request by checking the validity of
`x-slack-signature`, `x-slack-request-timestamp`, and its body data.

Refer to https://docs.slack.dev/authentication/verifying-requests-from-slack/ for details.

**Arguments**:

- `signing_secret` - The signing secret
- `base_logger` - The base logger

#### verifier

```python
@property
def verifier() -> SignatureVerifier
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

