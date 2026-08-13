---
sidebar_label: authorize_result
title: slack_bolt.authorization.authorize_result
---

## AuthorizeResult Objects

```python
class AuthorizeResult(dict)
```

Authorize function call result

#### enterprise\_id

#### team\_id

#### team

since v1.18

#### url

since v1.18

#### bot\_id

#### bot\_user\_id

#### bot\_token

#### bot\_scopes

since v1.17

#### user\_id

#### user

since v1.18

#### user\_token

#### user\_scopes

since v1.17

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

