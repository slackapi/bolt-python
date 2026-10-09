---
sidebar_label: oauth_flow
title: slack_bolt.oauth.oauth_flow
---

## `OAuthFlow`

```python
OAuthFlow(*, client=None, logger=None, settings)
```

The module to run the Slack app installation flow (OAuth flow).

**Parameters:**

- **client** (Optional[WebClient]) – The `slack_sdk.web.WebClient` instance.
- **logger** (Optional[Logger]) – The logger.
- **settings** (OAuthSettings) – OAuth settings to configure this module.
