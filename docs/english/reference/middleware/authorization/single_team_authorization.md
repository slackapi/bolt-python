---
sidebar_label: single_team_authorization
title: slack_bolt.middleware.authorization.single_team_authorization
---

## `SingleTeamAuthorization`

```python
SingleTeamAuthorization(*, auth_test_result=None, base_logger=None, user_facing_authorize_error_message=None)
```

Bases: Authorization

Single-workspace authorization.

**Parameters:**

- **auth_test_result** (Optional[SlackResponse]) – The initial `auth.test` API call result.
- **base_logger** (Optional[Logger]) – The base logger
- **user_facing_authorize_error_message** (Optional[str]) – The message shown to the end-user when authorization fails

### `name`

```python
name: str
```

The name of this middleware.
