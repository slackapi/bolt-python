---
sidebar_label: authorization
title: slack_bolt.middleware.authorization
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

## Submodules

- [slack_bolt.middleware.authorization.async_authorization](/tools/bolt-python/reference/middleware/authorization/async_authorization)
- [slack_bolt.middleware.authorization.async_internals](/tools/bolt-python/reference/middleware/authorization/async_internals)
- [slack_bolt.middleware.authorization.async_multi_teams_authorization](/tools/bolt-python/reference/middleware/authorization/async_multi_teams_authorization)
- [slack_bolt.middleware.authorization.async_single_team_authorization](/tools/bolt-python/reference/middleware/authorization/async_single_team_authorization)
- [slack_bolt.middleware.authorization.authorization](/tools/bolt-python/reference/middleware/authorization/authorization)
- [slack_bolt.middleware.authorization.internals](/tools/bolt-python/reference/middleware/authorization/internals)
- [slack_bolt.middleware.authorization.multi_teams_authorization](/tools/bolt-python/reference/middleware/authorization/multi_teams_authorization)
- [slack_bolt.middleware.authorization.single_team_authorization](/tools/bolt-python/reference/middleware/authorization/single_team_authorization)
