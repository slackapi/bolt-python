---
sidebar_label: async_oauth_flow
title: slack_bolt.oauth.async_oauth_flow
---

## `AsyncOAuthFlow`

```python
AsyncOAuthFlow(*, client=None, logger=None, settings)
```

The module to run the Slack app installation flow (OAuth flow).

**Parameters:**

- **client** (Optional[AsyncWebClient]) – The `slack_sdk.web.async_client.AsyncWebClient` instance.
- **logger** (Optional[Logger]) – The logger.
- **settings** (AsyncOAuthSettings) – OAuth settings to configure this module.
