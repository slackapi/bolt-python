---
sidebar_label: base_context
title: slack_bolt.context.base_context
---

## BaseContext Objects

```python
class BaseContext(dict)
```

Context object associated with a request from Slack.

#### copyable\_standard\_property\_names

#### non\_copyable\_standard\_property\_names

#### standard\_property\_names

#### logger

```python
@property
def logger() -> Logger
```

The properly configured logger that is available for middleware/listeners.

#### token

```python
@property
def token() -> Optional[str]
```

The (bot/user) token resolved for this request.

#### enterprise\_id

```python
@property
def enterprise_id() -> Optional[str]
```

The Enterprise Grid Organization ID of this request.

#### is\_enterprise\_install

```python
@property
def is_enterprise_install() -> Optional[bool]
```

True if the request is associated with an Org-wide installation.

#### team\_id

```python
@property
def team_id() -> Optional[str]
```

The Workspace ID of this request.

#### user\_id

```python
@property
def user_id() -> Optional[str]
```

The user ID associated ith this request.

#### actor\_enterprise\_id

```python
@property
def actor_enterprise_id() -> Optional[str]
```

The action's actor's Enterprise Grid organization ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

#### actor\_team\_id

```python
@property
def actor_team_id() -> Optional[str]
```

The action's actor's workspace ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

#### actor\_user\_id

```python
@property
def actor_user_id() -> Optional[str]
```

The action's actor's user ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it's not guaranteed to have a valid ID for all events due to server-side inconsistency.

#### channel\_id

```python
@property
def channel_id() -> Optional[str]
```

The conversation ID associated with this request.

#### thread\_ts

```python
@property
def thread_ts() -> Optional[str]
```

The conversation thread's ID associated with this request.

#### response\_url

```python
@property
def response_url() -> Optional[str]
```

The `response_url` associated with this request.

#### matches

```python
@property
def matches() -> Optional[Tuple]
```

Returns all the matched parts in message listener's regexp

#### function\_execution\_id

```python
@property
def function_execution_id() -> Optional[str]
```

The `function_execution_id` associated with this request.
Only available for `function_executed` and interactivity events scoped to a custom step.

#### inputs

```python
@property
def inputs() -> Optional[Dict[str, Any]]
```

The `inputs` associated with this request.
Only available for `function_executed` and interactivity events scoped to a custom step.

#### authorize\_result

```python
@property
def authorize_result() -> Optional[AuthorizeResult]
```

The authorize result resolved for this request.

#### function\_bot\_access\_token

```python
@property
def function_bot_access_token() -> Optional[str]
```

The bot token resolved for this function request.
Only available for `function_executed` and interactivity events scoped to a custom step.

#### bot\_token

```python
@property
def bot_token() -> Optional[str]
```

The bot token resolved for this request.

#### bot\_id

```python
@property
def bot_id() -> Optional[str]
```

The bot ID resolved for this request.

#### bot\_user\_id

```python
@property
def bot_user_id() -> Optional[str]
```

The bot user ID resolved for this request.

#### user\_token

```python
@property
def user_token() -> Optional[str]
```

The user token resolved for this request.

#### set\_authorize\_result

```python
def set_authorize_result(authorize_result: AuthorizeResult)
```
