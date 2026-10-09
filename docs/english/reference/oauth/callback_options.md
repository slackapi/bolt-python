---
sidebar_label: callback_options
title: slack_bolt.oauth.callback_options
---

## `CallbackOptions`

```python
CallbackOptions(success, failure)
```

The configurations for OAuth flow.

**Parameters:**

- **success** (Callable[[SuccessArgs], BoltResponse]) – A handler for successful installation.
- **failure** (Callable[[FailureArgs], BoltResponse]) – A handler for any types of installation failures.

## `FailureArgs`

```python
FailureArgs(*, request, reason, error=None, suggested_status_code, settings, default)
```

The arguments for a failure function.

**Parameters:**

- **request** (BoltRequest) – The request.
- **reason** (str) – The response.
- **error** (Optional[Exception]) – An exception if exists.
- **suggested_status_code** (int) – The recommended HTTP status code for the failure.
- **settings** (OAuthSettings) – The settings for Slack OAuth flow.
- **default** (CallbackOptions) – The default `CallbackOptions`.

## `SuccessArgs`

```python
SuccessArgs(*, request, installation, settings, default)
```

The arguments for a success function.

**Parameters:**

- **request** (BoltRequest) – The request.
- **installation** (Installation) – The installation data.
- **settings** (OAuthSettings) – The settings for Slack OAuth flow.
- **default** (CallbackOptions) – The default `CallbackOptions`
