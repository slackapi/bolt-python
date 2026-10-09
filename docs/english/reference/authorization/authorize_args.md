---
sidebar_label: authorize_args
title: slack_bolt.authorization.authorize_args
---

## `AuthorizeArgs`

```python
AuthorizeArgs(*, context, enterprise_id, team_id, user_id)
```

The full list of the arguments passed to `authorize` function.

**Parameters:**

- **context** (BoltContext) – The request context
- **enterprise_id** (Optional[str]) – The Organization ID (Enterprise Grid)
- **team_id** (Optional[str]) – The workspace ID
- **user_id** (Optional[str]) – The request user ID
