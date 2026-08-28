---
sidebar_label: async_request_verification
title: slack_bolt.middleware.request_verification.async_request_verification
---

## AsyncRequestVerification Objects

```python
class AsyncRequestVerification(RequestVerification, AsyncMiddleware)
```

Verifies an incoming request from Slack.

Checks the validity of `x-slack-signature`, `x-slack-request-timestamp`, and the request body data.

Refer to https://docs.slack.dev/authentication/verifying-requests-from-slack/ for details.

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```
