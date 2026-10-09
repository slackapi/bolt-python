---
sidebar_label: multi_teams_authorization
title: slack_bolt.middleware.authorization.multi_teams_authorization
---

## `MultiTeamsAuthorization`

```python
MultiTeamsAuthorization(*, authorize, base_logger=None, user_token_resolution='authed_user', user_facing_authorize_error_message=None)
```

Bases: Authorization

Multi-workspace authorization.

**Parameters:**

- **authorize** (Authorize) – The function to authorize incoming requests from Slack.
- **base_logger** (Optional[Logger]) – The base logger
- **user_token_resolution** (str) – "authed_user" or "actor"
- **user_facing_authorize_error_message** (Optional[str]) – The user-facing error message when installation is not found

### `name`

```python
name: str
```

The name of this middleware.
