---
sidebar_label: async_callback_options
title: slack_bolt.oauth.async_callback_options
---

## `AsyncFailureArgs`

```python
AsyncFailureArgs(*, request, reason, error=None, suggested_status_code, settings, default)
```

The arguments for a failure function.

**Parameters:**

- **request** (AsyncBoltRequest) – The request.
- **reason** (str) – The response.
- **error** (Optional[Exception]) – An exception if exists.
- **suggested_status_code** (int) – The recommended HTTP status code for the failure.
- **settings** (AsyncOAuthSettings) – The settings for Slack OAuth flow.
- **default** (AsyncCallbackOptions) – The default `AsyncCallbackOptions`.

## `AsyncSuccessArgs`

```python
AsyncSuccessArgs(*, request, installation, settings, default)
```

The arguments for a success function.

**Parameters:**

- **request** (AsyncBoltRequest) – The request.
- **installation** (Installation) – The installation data.
- **settings** (AsyncOAuthSettings) – The settings for Slack OAuth flow.
- **default** (AsyncCallbackOptions) – The default `AsyncCallbackOptions`.
