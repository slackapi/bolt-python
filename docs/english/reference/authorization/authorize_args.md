---
sidebar_label: authorize_args
title: slack_bolt.authorization.authorize_args
---

## AuthorizeArgs Objects

```python
class AuthorizeArgs()
```

#### context: `BoltContext`

#### logger: `Logger`

#### client: `WebClient`

#### enterprise\_id: `Optional[str]`

#### team\_id: `Optional[str]`

#### user\_id: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(
    *,
    context: BoltContext,
    enterprise_id: Optional[str],
    team_id: Optional[str],
    user_id: Optional[str])
```

The full list of the arguments passed to `authorize` function.

**Arguments**:

- `context` _BoltContext_ - The request context
- `enterprise_id` _Optional[str]_ - The Organization ID (Enterprise Grid)
- `team_id` _Optional[str]_ - The workspace ID
- `user_id` _Optional[str]_ - The request user ID
