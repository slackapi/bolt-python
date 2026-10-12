---
sidebar_label: request_verification
title: slack_bolt.middleware.request_verification
---

## `RequestVerification`

```python
RequestVerification(signing_secret, base_logger=None)
```

Bases: Middleware

Verifies an incoming request from Slack.

Checks the validity of `x-slack-signature`, `x-slack-request-timestamp`, and the request body data.

Refer to https://docs.slack.dev/authentication/verifying-requests-from-slack/ for details.

**Parameters:**

- **signing_secret** (str) – The signing secret
- **base_logger** (Optional[Logger]) – The base logger

### `name`

```python
name: str
```

The name of this middleware.

## Submodules

- [slack_bolt.middleware.request_verification.async_request_verification](/tools/bolt-python/reference/middleware/request_verification/async_request_verification)
- [slack_bolt.middleware.request_verification.request_verification](/tools/bolt-python/reference/middleware/request_verification/request_verification)
