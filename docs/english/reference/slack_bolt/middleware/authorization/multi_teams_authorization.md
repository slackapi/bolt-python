---
sidebar_label: multi_teams_authorization
title: slack_bolt.middleware.authorization.multi_teams_authorization
---

#### get\_bolt\_logger

```python
def get_bolt_logger(cls: Any, base_logger: Optional[Logger] = None) -> Logger
```

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body

#### query

#### headers

#### content\_type

#### body

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

#### first\_headers

```python
def first_headers() -> Dict[str, str]
```

#### first\_headers\_without\_set\_cookie

```python
def first_headers_without_set_cookie() -> Dict[str, str]
```

#### cookies

```python
def cookies() -> Sequence[SimpleCookie]
```

## Authorization Objects

```python
class Authorization(Middleware)
```

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

## Authorize Objects

```python
class Authorize()
```

This provides authorize function that returns AuthorizeResult
for an incoming request from Slack.

## MultiTeamsAuthorization Objects

```python
class MultiTeamsAuthorization(Authorization)
```

#### authorize

#### user\_token\_resolution

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

