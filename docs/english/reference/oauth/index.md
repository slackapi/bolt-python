---
sidebar_label: oauth
title: slack_bolt.oauth
---

Slack OAuth flow support for building an app that is installable in any workspaces.

Refer to https://docs.slack.dev/tools/bolt-python/concepts/authenticating-oauth for details.

## `OAuthFlow`

```python
OAuthFlow(*, client=None, logger=None, settings)
```

The module to run the Slack app installation flow (OAuth flow).

**Parameters:**

- **client** (Optional[WebClient]) – The `slack_sdk.web.WebClient` instance.
- **logger** (Optional[Logger]) – The logger.
- **settings** (OAuthSettings) – OAuth settings to configure this module.

## Submodules

- [slack_bolt.oauth.async_callback_options](/tools/bolt-python/reference/oauth/async_callback_options)
- [slack_bolt.oauth.async_internals](/tools/bolt-python/reference/oauth/async_internals)
- [slack_bolt.oauth.async_oauth_flow](/tools/bolt-python/reference/oauth/async_oauth_flow)
- [slack_bolt.oauth.async_oauth_settings](/tools/bolt-python/reference/oauth/async_oauth_settings)
- [slack_bolt.oauth.callback_options](/tools/bolt-python/reference/oauth/callback_options)
- [slack_bolt.oauth.internals](/tools/bolt-python/reference/oauth/internals)
- [slack_bolt.oauth.oauth_flow](/tools/bolt-python/reference/oauth/oauth_flow)
- [slack_bolt.oauth.oauth_settings](/tools/bolt-python/reference/oauth/oauth_settings)
