---
sidebar_label: authorization
title: slack_bolt.authorization
---

Authorization determines which Slack credentials should be available while processing an incoming Slack event.

Refer to https://docs.slack.dev/tools/bolt-python/concepts/authorization for details.

## Submodules

- [slack_bolt.authorization.async_authorize](/tools/bolt-python/reference/authorization/async_authorize)
- [slack_bolt.authorization.async_authorize_args](/tools/bolt-python/reference/authorization/async_authorize_args)
- [slack_bolt.authorization.authorize](/tools/bolt-python/reference/authorization/authorize)
- [slack_bolt.authorization.authorize_args](/tools/bolt-python/reference/authorization/authorize_args)
- [slack_bolt.authorization.authorize_result](/tools/bolt-python/reference/authorization/authorize_result)

## AuthorizeResult Objects

```python
class AuthorizeResult(dict)
```

Authorize function call result.

#### enterprise\_id: `Optional[str]`

#### team\_id: `Optional[str]`

#### team: `Optional[str]`

#### url: `Optional[str]`

#### bot\_id: `Optional[str]`

#### bot\_user\_id: `Optional[str]`

#### bot\_token: `Optional[str]`

#### bot\_scopes: `Optional[Sequence[str]]`

#### user\_id: `Optional[str]`

#### user: `Optional[str]`

#### user\_token: `Optional[str]`

#### user\_scopes: `Optional[Sequence[str]]`

#### \_\_init\_\_

```python
def __init__(
    *,
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

Initialize the authorize function call result.

**Arguments**:

- `enterprise_id` _Optional[str]_ - Organization ID (Enterprise Grid) starting with `E`
- `team_id` _Optional[str]_ - Workspace ID starting with `T`
- `team` _Optional[str]_ - Workspace name
- `url` _Optional[str]_ - Workspace slack.com URL
- `bot_user_id` _Optional[str]_ - Bot user's User ID starting with either `U` or `W`
- `bot_id` _Optional[str]_ - Bot ID starting with `B`
- `bot_token` _Optional[str]_ - Bot user access token starting with `xoxb-`
- `bot_scopes` _Optional[Union[Sequence[str], str]]_ - The scopes associated with the bot token
- `user_id` _Optional[str]_ - The request user ID
- `user` _Optional[str]_ - The request user's name
- `user_token` _Optional[str]_ - User access token starting with `xoxp-`
- `user_scopes` _Optional[Union[Sequence[str], str]]_ - The scopes associated with the user token

#### from\_auth\_test\_response

```python
def from_auth_test_response(
    *,
    bot_token: Optional[str] = None,
    user_token: Optional[str] = None,
    bot_scopes: Optional[Union[Sequence[str], str]] = None,
    user_scopes: Optional[Union[Sequence[str], str]] = None,
    auth_test_response: Union[SlackResponse, AsyncSlackResponse],
    user_auth_test_response: Optional[Union[SlackResponse, AsyncSlackResponse]] = None) -> AuthorizeResult
```
