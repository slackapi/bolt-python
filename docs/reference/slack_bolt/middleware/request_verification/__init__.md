---
sidebar_label: request_verification
title: slack_bolt.middleware.request_verification
---

## RequestVerification Objects

```python
class RequestVerification(Middleware)
```

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

