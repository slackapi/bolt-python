---
sidebar_label: async_request_verification
title: slack_bolt.middleware.request_verification.async_request_verification
---

## `AsyncRequestVerification`

Bases: RequestVerification, AsyncMiddleware

Verifies an incoming request from Slack.

Checks the validity of `x-slack-signature`, `x-slack-request-timestamp`, and the request body data.

Refer to https://docs.slack.dev/authentication/verifying-requests-from-slack/ for details.

### `name`

```python
name: str
```

The name of this middleware.
