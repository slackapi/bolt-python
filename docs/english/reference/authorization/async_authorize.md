---
sidebar_label: async_authorize
title: slack_bolt.authorization.async_authorize
---

## `AsyncAuthorize`

```python
AsyncAuthorize()
```

This provides authorize function that returns AuthorizeResult for an incoming request from Slack.

## `AsyncCallableAuthorize`

```python
AsyncCallableAuthorize(*, logger, func)
```

Bases: AsyncAuthorize

When you pass the `authorize` argument in AsyncApp constructor, this `authorize` implementation will be used.

## `AsyncInstallationStoreAuthorize`

```python
AsyncInstallationStoreAuthorize(*, logger, installation_store, client_id=None, client_secret=None, token_rotation_expiration_minutes=None, bot_only=False, cache_enabled=False, client=None, user_token_resolution='authed_user')
```

Bases: AsyncAuthorize

If you use the OAuth flow settings, this authorize implementation will be used.

As long as your own InstallationStore (or the built-in ones) works as you expect,
you can expect that the authorize layer should work for you without any customization.
