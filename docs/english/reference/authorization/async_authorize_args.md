---
sidebar_label: async_authorize_args
title: slack_bolt.authorization.async_authorize_args
---

## `AsyncAuthorizeArgs`

```python
AsyncAuthorizeArgs(*, context, enterprise_id, team_id, user_id)
```

The full list of the arguments passed to `authorize` function.

**Parameters:**

- **context** (AsyncBoltContext) – The request context
- **enterprise_id** (Optional[str]) – The Organization ID (Enterprise Grid)
- **team_id** (Optional[str]) – The workspace ID
- **user_id** (Optional[str]) – The request user ID
