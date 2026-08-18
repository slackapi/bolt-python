---
sidebar_label: callback_options
title: slack_bolt.oauth.callback_options
---

## CallbackResponseBuilder Objects

```python
class CallbackResponseBuilder()
```

#### \_\_init\_\_

```python
def __init__(*, logger: Logger, state_utils: OAuthStateUtils,
             redirect_uri_page_renderer: RedirectUriPageRenderer)
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

## SuccessArgs Objects

```python
class SuccessArgs()
```

#### \_\_init\_\_

```python
def __init__(*, request: BoltRequest, installation: Installation,
             settings: "OAuthSettings", default: "CallbackOptions")
```

The arguments for a success function.

**Arguments**:

- `request` - The request.
- `installation` - The installation data.
- `settings` - The settings for Slack OAuth flow.
- `default` - The default `CallbackOptions`

## FailureArgs Objects

```python
class FailureArgs()
```

#### \_\_init\_\_

```python
def __init__(*,
             request: BoltRequest,
             reason: str,
             error: Optional[Exception] = None,
             suggested_status_code: int,
             settings: "OAuthSettings",
             default: "CallbackOptions")
```

The arguments for a failure function.

**Arguments**:

- `request` - The request.
- `reason` - The response.
- `error` - An exception if exists.
- `suggested_status_code` - The recommended HTTP status code for the failure.
- `settings` - The settings for Slack OAuth flow.
- `default` - The default `CallbackOptions`.

## CallbackOptions Objects

```python
class CallbackOptions()
```

#### success: `Callable[[SuccessArgs], BoltResponse]`

A handler for successful installation.

#### failure: `Callable[[FailureArgs], BoltResponse]`

A handler for any types of installation failures.

#### \_\_init\_\_

```python
def __init__(success: Callable[[SuccessArgs], BoltResponse],
             failure: Callable[[FailureArgs], BoltResponse])
```

The configurations for OAuth flow.

**Arguments**:

- `success` - A handler for successful installation.
- `failure` - A handler for any types of installation failures.

## DefaultCallbackOptions Objects

```python
class DefaultCallbackOptions(CallbackOptions)
```

#### success: `Callable[[SuccessArgs], BoltResponse]`

#### failure: `Callable[[FailureArgs], BoltResponse]`

#### \_\_init\_\_

```python
def __init__(*, logger: Logger, state_utils: OAuthStateUtils,
             redirect_uri_page_renderer: RedirectUriPageRenderer)
```

