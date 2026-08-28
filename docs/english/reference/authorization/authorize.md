---
sidebar_label: authorize
title: slack_bolt.authorization.authorize
---

## `Authorize`

```python
Authorize()
```

This provides authorize function that returns AuthorizeResult for an incoming request from Slack.

## `CallableAuthorize`

```python
CallableAuthorize(*, logger, func)
```

Bases: Authorize

When you pass the `authorize` argument in App constructor, this `authorize` implementation will be used.

## `InstallationStoreAuthorize`

```python
InstallationStoreAuthorize(*, logger, installation_store, client_id=None, client_secret=None, token_rotation_expiration_minutes=None, bot_only=False, cache_enabled=False, client=None, user_token_resolution='authed_user')
```

Bases: Authorize

If you use the OAuth flow settings, this `authorize` implementation will be used.

As long as your own InstallationStore (or the built-in ones) works as you expect,
you can expect that the `authorize` layer should work for you without any customization.
