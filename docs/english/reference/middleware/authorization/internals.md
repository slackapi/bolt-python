---
sidebar_label: internals
title: slack_bolt.middleware.authorization.internals
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

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body: `str`

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### context: `BoltContext`

The context in this request.

#### lazy\_only: `bool`

#### lazy\_function\_name: `Optional[str]`

#### mode: `str`

The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

#### \_\_init\_\_

```python
def __init__(*,
             body: Union[str, dict],
             query: Optional[Union[str, Dict[str, str],
                                   Dict[str, Sequence[str]]]] = None,
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
             context: Optional[Dict[str, Any]] = None,
             mode: str = "http")
```

Request to a Bolt app.

**Arguments**:

- `body` - The raw request body (only plain text is supported for &quot;http&quot; mode)
- `query` - The query string data in any data format.
- `headers` - The request headers.
- `context` - The context in this request.
- `mode` - The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status: `int`

HTTP status code

#### body: `str`

The response body (dict and str are supported)

#### headers: `Dict[str, Sequence[str]]`

The response headers.

#### \_\_init\_\_

```python
def __init__(*,
             status: int,
             body: Union[str, dict] = "",
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None)
```

The response from a Bolt app.

**Arguments**:

- `status` - HTTP status code
- `body` - The response body (dict and str are supported)
- `headers` - The response headers.

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

#### no\_auth\_test\_events

