---
sidebar_label: ssl_check
title: slack_bolt.middleware.ssl_check.ssl_check
slug: ssl_check
---

## `SslCheck`

```python
SslCheck(verification_token=None, base_logger=None)
```

Bases: Middleware

Handles `ssl_check` requests.

Refer to https://docs.slack.dev/interactivity/implementing-slash-commands/ for details.

**Parameters:**

- **verification_token** (Optional[str]) – The verification token to check
(optional as it's already deprecated - https://docs.slack.dev/authentication/verifying-requests-from-slack/#deprecation)
- **base_logger** (Optional[Logger]) – The base logger

### `name`

```python
name: str
```

The name of this middleware.
