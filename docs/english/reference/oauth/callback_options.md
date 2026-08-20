---
sidebar_label: callback_options
title: slack_bolt.oauth.callback_options
---

## SuccessArgs Objects

```python
class SuccessArgs()
```

#### \_\_init\_\_

```python
def __init__(
    *,
    request: BoltRequest,
    installation: Installation,
    settings: OAuthSettings,
    default: CallbackOptions)
```

The arguments for a success function.

**Arguments**:

- `request` _BoltRequest_ - The request.
- `installation` _Installation_ - The installation data.
- `settings` _OAuthSettings_ - The settings for Slack OAuth flow.
- `default` _CallbackOptions_ - The default `CallbackOptions`

## FailureArgs Objects

```python
class FailureArgs()
```

#### \_\_init\_\_

```python
def __init__(
    *,
    request: BoltRequest,
    reason: str,
    error: Optional[Exception] = None,
    suggested_status_code: int,
    settings: OAuthSettings,
    default: CallbackOptions)
```

The arguments for a failure function.

**Arguments**:

- `request` _BoltRequest_ - The request.
- `reason` _str_ - The response.
- `error` _Optional[Exception]_ - An exception if exists.
- `suggested_status_code` _int_ - The recommended HTTP status code for the failure.
- `settings` _OAuthSettings_ - The settings for Slack OAuth flow.
- `default` _CallbackOptions_ - The default `CallbackOptions`.

## CallbackOptions Objects

```python
class CallbackOptions()
```

#### success: `Callable[[SuccessArgs], BoltResponse]`

#### failure: `Callable[[FailureArgs], BoltResponse]`

#### \_\_init\_\_

```python
def __init__(
    success: Callable[[SuccessArgs], BoltResponse],
    failure: Callable[[FailureArgs], BoltResponse])
```

The configurations for OAuth flow.

**Arguments**:

- `success` _Callable[[SuccessArgs], BoltResponse]_ - A handler for successful installation.
- `failure` _Callable[[FailureArgs], BoltResponse]_ - A handler for any types of installation failures.

## DefaultCallbackOptions Objects

```python
class DefaultCallbackOptions(CallbackOptions)
```

#### success: `Callable[[SuccessArgs], BoltResponse]`

#### failure: `Callable[[FailureArgs], BoltResponse]`

#### \_\_init\_\_

```python
def __init__(
    *,
    logger: Logger,
    state_utils: OAuthStateUtils,
    redirect_uri_page_renderer: RedirectUriPageRenderer)
```
