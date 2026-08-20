---
sidebar_label: async_single_team_authorization
title: slack_bolt.middleware.authorization.async_single_team_authorization
---

## AsyncSingleTeamAuthorization Objects

```python
class AsyncSingleTeamAuthorization(AsyncAuthorization)
```

#### \_\_init\_\_

```python
def __init__(
    base_logger: Optional[Logger] = None,
    user_facing_authorize_error_message: Optional[str] = None)
```

Single-workspace authorization.

#### auth\_test\_result: `Optional[AsyncSlackResponse]`

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> BoltResponse
```
