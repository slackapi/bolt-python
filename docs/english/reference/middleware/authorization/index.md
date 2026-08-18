---
sidebar_label: authorization
title: slack_bolt.middleware.authorization
---

## Submodules

- [slack_bolt.middleware.authorization.async_authorization](/tools/bolt-python/reference/middleware/authorization/async_authorization)
- [slack_bolt.middleware.authorization.async_internals](/tools/bolt-python/reference/middleware/authorization/async_internals)
- [slack_bolt.middleware.authorization.async_multi_teams_authorization](/tools/bolt-python/reference/middleware/authorization/async_multi_teams_authorization)
- [slack_bolt.middleware.authorization.async_single_team_authorization](/tools/bolt-python/reference/middleware/authorization/async_single_team_authorization)
- [slack_bolt.middleware.authorization.authorization](/tools/bolt-python/reference/middleware/authorization/authorization)
- [slack_bolt.middleware.authorization.internals](/tools/bolt-python/reference/middleware/authorization/internals)
- [slack_bolt.middleware.authorization.multi_teams_authorization](/tools/bolt-python/reference/middleware/authorization/multi_teams_authorization)
- [slack_bolt.middleware.authorization.single_team_authorization](/tools/bolt-python/reference/middleware/authorization/single_team_authorization)

## Authorization Objects

```python
class Authorization(Middleware)
```

## MultiTeamsAuthorization Objects

```python
class MultiTeamsAuthorization(Authorization)
```

#### authorize: `Authorize`

The function to authorize incoming requests from Slack.

#### user\_token\_resolution: `str`

Either &quot;authed_user&quot; or &quot;actor&quot;.

#### \_\_init\_\_

```python
def __init__(*,
             authorize: Authorize,
             base_logger: Optional[Logger] = None,
             user_token_resolution: str = "authed_user",
             user_facing_authorize_error_message: Optional[str] = None)
```

Multi-workspace authorization.

**Arguments**:

- `authorize` - The function to authorize incoming requests from Slack.
- `base_logger` - The base logger
- `user_token_resolution` - &quot;authed_user&quot; or &quot;actor&quot;
- `user_facing_authorize_error_message` - The user-facing error message when installation is not found

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

## SingleTeamAuthorization Objects

```python
class SingleTeamAuthorization(Authorization)
```

#### \_\_init\_\_

```python
def __init__(*,
             auth_test_result: Optional[SlackResponse] = None,
             base_logger: Optional[Logger] = None,
             user_facing_authorize_error_message: Optional[str] = None)
```

Single-workspace authorization.

**Arguments**:

- `auth_test_result` - The initial `auth.test` API call result.
- `base_logger` - The base logger

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

