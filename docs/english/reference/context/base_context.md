---
sidebar_label: base_context
title: slack_bolt.context.base_context
---

## AuthorizeResult Objects

```python
class AuthorizeResult(dict)
```

Authorize function call result

#### enterprise\_id: `Optional[str]`

Organization ID (Enterprise Grid) starting with `E`

#### team\_id: `Optional[str]`

Workspace ID starting with `T`

#### team: `Optional[str]`

Workspace name

#### url: `Optional[str]`

Workspace slack.com URL

#### bot\_id: `Optional[str]`

Bot ID starting with `B`

#### bot\_user\_id: `Optional[str]`

Bot user&#x27;s User ID starting with either `U` or `W`

#### bot\_token: `Optional[str]`

Bot user access token starting with `xoxb-`

#### bot\_scopes: `Optional[Sequence[str]]`

The scopes associated with the bot token

#### user\_id: `Optional[str]`

The request user ID

#### user: `Optional[str]`

The request user&#x27;s name

#### user\_token: `Optional[str]`

User access token starting with `xoxp-`

#### user\_scopes: `Optional[Sequence[str]]`

The scopes associated wth the user token

#### \_\_init\_\_

```python
def __init__(*,
             enterprise_id: Optional[str],
             team_id: Optional[str],
             team: Optional[str] = None,
             url: Optional[str] = None,
             bot_user_id: Optional[str] = None,
             bot_id: Optional[str] = None,
             bot_token: Optional[str] = None,
             bot_scopes: Optional[Union[Sequence[str], str]] = None,
             user_id: Optional[str] = None,
             user: Optional[str] = None,
             user_token: Optional[str] = None,
             user_scopes: Optional[Union[Sequence[str], str]] = None)
```

**Arguments**:

- `enterprise_id` - Organization ID (Enterprise Grid) starting with `E`
- `team_id` - Workspace ID starting with `T`
- `team` - Workspace name
- `url` - Workspace slack.com URL
- `bot_user_id` - Bot user&#x27;s User ID starting with either `U` or `W`
- `bot_id` - Bot ID starting with `B`
- `bot_token` - Bot user access token starting with `xoxb-`
- `bot_scopes` - The scopes associated with the bot token
- `user_id` - The request user ID
- `user` - The request user&#x27;s name
- `user_token` - User access token starting with `xoxp-`
- `user_scopes` - The scopes associated wth the user token

#### from\_auth\_test\_response

```python
@classmethod
def from_auth_test_response(
    cls,
    *,
    bot_token: Optional[str] = None,
    user_token: Optional[str] = None,
    bot_scopes: Optional[Union[Sequence[str], str]] = None,
    user_scopes: Optional[Union[Sequence[str], str]] = None,
    auth_test_response: Union[SlackResponse, "AsyncSlackResponse"],
    user_auth_test_response: Optional[Union[SlackResponse,
                                            "AsyncSlackResponse"]] = None
) -> "AuthorizeResult"
```

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

The action&#x27;s actor&#x27;s Enterprise Grid organization ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it&#x27;s not guaranteed to have a valid ID for all events due to server-side inconsistency.

#### actor\_team\_id

```python
@property
def actor_team_id() -> Optional[str]
```

The action&#x27;s actor&#x27;s workspace ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it&#x27;s not guaranteed to have a valid ID for all events due to server-side inconsistency.

#### actor\_user\_id

```python
@property
def actor_user_id() -> Optional[str]
```

The action&#x27;s actor&#x27;s user ID.
Note that this property is especially useful for handling events in Slack Connect channels.
That being said, it&#x27;s not guaranteed to have a valid ID for all events due to server-side inconsistency.

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

The conversation thread&#x27;s ID associated with this request.

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

Returns all the matched parts in message listener&#x27;s regexp

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

