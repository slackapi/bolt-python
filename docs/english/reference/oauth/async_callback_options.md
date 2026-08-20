---
sidebar_label: async_callback_options
title: slack_bolt.oauth.async_callback_options
---

## AsyncSuccessArgs Objects

```python
class AsyncSuccessArgs()
```

#### \_\_init\_\_

```python
def __init__(
    *,
    request: AsyncBoltRequest,
    installation: Installation,
    settings: AsyncOAuthSettings,
    default: AsyncCallbackOptions)
```

The arguments for a success function.

**Arguments**:

- `request` _AsyncBoltRequest_ - The request.
- `installation` _Installation_ - The installation data.
- `settings` _AsyncOAuthSettings_ - The settings for Slack OAuth flow.
- `default` _AsyncCallbackOptions_ - The default `AsyncCallbackOptions`.

## AsyncFailureArgs Objects

```python
class AsyncFailureArgs()
```

#### \_\_init\_\_

```python
def __init__(
    *,
    request: AsyncBoltRequest,
    reason: str,
    error: Optional[Exception] = None,
    suggested_status_code: int,
    settings: AsyncOAuthSettings,
    default: AsyncCallbackOptions)
```

The arguments for a failure function.

**Arguments**:

- `request` _AsyncBoltRequest_ - The request.
- `reason` _str_ - The response.
- `error` _Optional[Exception]_ - An exception if exists.
- `suggested_status_code` _int_ - The recommended HTTP status code for the failure.
- `settings` _AsyncOAuthSettings_ - The settings for Slack OAuth flow.
- `default` _AsyncCallbackOptions_ - The default `AsyncCallbackOptions`.

## AsyncCallbackOptions Objects

```python
class AsyncCallbackOptions()
```

#### success: `Callable[[AsyncSuccessArgs], Awaitable[BoltResponse]]`

#### failure: `Callable[[AsyncFailureArgs], Awaitable[BoltResponse]]`

#### \_\_init\_\_

```python
def __init__(
    success: Callable[[AsyncSuccessArgs], Awaitable[BoltResponse]],
    failure: Callable[[AsyncFailureArgs], Awaitable[BoltResponse]])
```

## DefaultAsyncCallbackOptions Objects

```python
class DefaultAsyncCallbackOptions(AsyncCallbackOptions)
```

#### success: `Callable[[AsyncSuccessArgs], Awaitable[BoltResponse]]`

#### failure: `Callable[[AsyncFailureArgs], Awaitable[BoltResponse]]`

#### \_\_init\_\_

```python
def __init__(
    *,
    logger: Logger,
    state_utils: OAuthStateUtils,
    redirect_uri_page_renderer: RedirectUriPageRenderer)
```
