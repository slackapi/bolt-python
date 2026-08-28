---
sidebar_label: single_team_authorization
title: slack_bolt.middleware.authorization.single_team_authorization
---

## SingleTeamAuthorization Objects

```python
class SingleTeamAuthorization(Authorization)
```

#### \_\_init\_\_

```python
def __init__(
    *,
    auth_test_result: Optional[SlackResponse] = None,
    base_logger: Optional[Logger] = None,
    user_facing_authorize_error_message: Optional[str] = None)
```

Single-workspace authorization.

**Arguments**:

- `auth_test_result` _Optional[SlackResponse]_ - The initial `auth.test` API call result.
- `base_logger` _Optional[Logger]_ - The base logger
- `user_facing_authorize_error_message` _Optional[str]_ - The message shown to the end-user when authorization fails

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> BoltResponse
```
