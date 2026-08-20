---
sidebar_label: multi_teams_authorization
title: slack_bolt.middleware.authorization.multi_teams_authorization
---

## MultiTeamsAuthorization Objects

```python
class MultiTeamsAuthorization(Authorization)
```

#### authorize: `Authorize`

#### user\_token\_resolution: `str`

#### \_\_init\_\_

```python
def __init__(
    *,
    authorize: Authorize,
    base_logger: Optional[Logger] = None,
    user_token_resolution: str = 'authed_user',
    user_facing_authorize_error_message: Optional[str] = None)
```

Multi-workspace authorization.

**Arguments**:

- `authorize` _Authorize_ - The function to authorize incoming requests from Slack.
- `base_logger` _Optional[Logger]_ - The base logger
- `user_token_resolution` _str_ - "authed_user" or "actor"
- `user_facing_authorize_error_message` _Optional[str]_ - The user-facing error message when installation is not found

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> BoltResponse
```
