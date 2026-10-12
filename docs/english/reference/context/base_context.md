---
sidebar_label: base_context
title: slack_bolt.context.base_context
---

## `BaseContext`

Bases: dict

Context object associated with a request from Slack.

### `actor_enterprise_id`

```python
actor_enterprise_id: Optional[str]
```

The action's actor's Enterprise Grid organization ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `actor_team_id`

```python
actor_team_id: Optional[str]
```

The action's actor's workspace ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `actor_user_id`

```python
actor_user_id: Optional[str]
```

The action's actor's user ID.

Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

### `authorize_result`

```python
authorize_result: Optional[AuthorizeResult]
```

The authorize result resolved for this request.

### `bot_id`

```python
bot_id: Optional[str]
```

The bot ID resolved for this request.

### `bot_token`

```python
bot_token: Optional[str]
```

The bot token resolved for this request.

### `bot_user_id`

```python
bot_user_id: Optional[str]
```

The bot user ID resolved for this request.

### `channel_id`

```python
channel_id: Optional[str]
```

The conversation ID associated with this request.

### `enterprise_id`

```python
enterprise_id: Optional[str]
```

The Enterprise Grid Organization ID of this request.

### `function_bot_access_token`

```python
function_bot_access_token: Optional[str]
```

The bot token resolved for this function request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `function_execution_id`

```python
function_execution_id: Optional[str]
```

The `function_execution_id` associated with this request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `inputs`

```python
inputs: Optional[Dict[str, Any]]
```

The `inputs` associated with this request.

Only available for `function_executed` and interactivity events scoped to a custom step.

### `is_enterprise_install`

```python
is_enterprise_install: Optional[bool]
```

True if the request is associated with an Org-wide installation.

### `logger`

```python
logger: Logger
```

The properly configured logger that is available for middleware/listeners.

### `matches`

```python
matches: Optional[Tuple]
```

Returns all the matched parts in message listener's regexp.

### `response_url`

```python
response_url: Optional[str]
```

The `response_url` associated with this request.

### `team_id`

```python
team_id: Optional[str]
```

The Workspace ID of this request.

### `thread_ts`

```python
thread_ts: Optional[str]
```

The conversation thread's ID associated with this request.

### `token`

```python
token: Optional[str]
```

The (bot/user) token resolved for this request.

### `user_id`

```python
user_id: Optional[str]
```

The user ID associated ith this request.

### `user_token`

```python
user_token: Optional[str]
```

The user token resolved for this request.
