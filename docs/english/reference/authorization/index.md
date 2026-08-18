---
sidebar_label: authorization
title: slack_bolt.authorization
---


Authorization is the process of determining which Slack credentials should be available
while processing an incoming Slack event.

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

Authorize function call result

#### enterprise\_id

Organization ID (Enterprise Grid) starting with `E`

#### team\_id

Workspace ID starting with `T`

#### team

Workspace name

#### url

Workspace slack.com URL

#### bot\_id

Bot ID starting with `B`

#### bot\_user\_id

Bot user&#x27;s User ID starting with either `U` or `W`

#### bot\_token

Bot user access token starting with `xoxb-`

#### bot\_scopes

The scopes associated with the bot token

#### user\_id

The request user ID

#### user

The request user&#x27;s name

#### user\_token

User access token starting with `xoxp-`

#### user\_scopes

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

