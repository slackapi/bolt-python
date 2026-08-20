---
sidebar_label: async_authorize
title: slack_bolt.authorization.async_authorize
---

## AsyncAuthorize Objects

```python
class AsyncAuthorize()
```

This provides authorize function that returns AuthorizeResult
for an incoming request from Slack.

#### \_\_init\_\_

```python
def __init__()
```

## AsyncCallableAuthorize Objects

```python
class AsyncCallableAuthorize(AsyncAuthorize)
```

When you pass the authorize argument in AsyncApp constructor,
This authorize implementation will be used.

#### \_\_init\_\_

```python
def __init__(*, logger: Logger, func: Callable[..., Awaitable[AuthorizeResult]])
```

## AsyncInstallationStoreAuthorize Objects

```python
class AsyncInstallationStoreAuthorize(AsyncAuthorize)
```

If you use the OAuth flow settings, this authorize implementation will be used.
As long as your own InstallationStore (or the built-in ones) works as you expect,
you can expect that the authorize layer should work for you without any customization.

#### authorize\_result\_cache: `Dict[str, AuthorizeResult]`

#### bot\_only: `bool`

#### user\_token\_resolution: `str`

#### find\_installation\_available: `Optional[bool]`

#### find\_bot\_available: `Optional[bool]`

#### token\_rotator: `Optional[AsyncTokenRotator]`

#### \_\_init\_\_

```python
def __init__(
    *,
    logger: Logger,
    installation_store: AsyncInstallationStore,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    token_rotation_expiration_minutes: Optional[int] = None,
    bot_only: bool = False,
    cache_enabled: bool = False,
    client: Optional[AsyncWebClient] = None,
    user_token_resolution: str = 'authed_user')
```
