---
sidebar_label: authorize
title: slack_bolt.authorization.authorize
---

## Authorize Objects

```python
class Authorize()
```

This provides authorize function that returns AuthorizeResult for an incoming request from Slack.

#### \_\_init\_\_

```python
def __init__()
```

## CallableAuthorize Objects

```python
class CallableAuthorize(Authorize)
```

When you pass the `authorize` argument in App constructor, this `authorize` implementation will be used.

#### \_\_init\_\_

```python
def __init__(*, logger: Logger, func: Callable[..., AuthorizeResult])
```

## InstallationStoreAuthorize Objects

```python
class InstallationStoreAuthorize(Authorize)
```

If you use the OAuth flow settings, this `authorize` implementation will be used.

As long as your own InstallationStore (or the built-in ones) works as you expect,
you can expect that the `authorize` layer should work for you without any customization.

#### authorize\_result\_cache: `Dict[str, AuthorizeResult]`

#### bot\_only: `bool`

#### user\_token\_resolution: `str`

#### find\_installation\_available: `bool`

#### find\_bot\_available: `bool`

#### token\_rotator: `Optional[TokenRotator]`

#### \_\_init\_\_

```python
def __init__(
    *,
    logger: Logger,
    installation_store: InstallationStore,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    token_rotation_expiration_minutes: Optional[int] = None,
    bot_only: bool = False,
    cache_enabled: bool = False,
    client: Optional[WebClient] = None,
    user_token_resolution: str = 'authed_user')
```
