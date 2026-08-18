---
sidebar_label: async_callback_options
title: slack_bolt.oauth.async_callback_options
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

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body: `str`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### context: `AsyncBoltContext`

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
def to_copyable() -> "AsyncBoltRequest"
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

## AsyncSuccessArgs Objects

```python
class AsyncSuccessArgs()
```

#### \_\_init\_\_

```python
def __init__(*, request: AsyncBoltRequest, installation: Installation,
             settings: "AsyncOAuthSettings", default: "AsyncCallbackOptions")
```

The arguments for a success function.

**Arguments**:

- `request` - The request.
- `installation` - The installation data.
- `settings` - The settings for Slack OAuth flow.
- `default` - The default `AsyncCallbackOptions`.

## AsyncFailureArgs Objects

```python
class AsyncFailureArgs()
```

#### \_\_init\_\_

```python
def __init__(*,
             request: AsyncBoltRequest,
             reason: str,
             error: Optional[Exception] = None,
             suggested_status_code: int,
             settings: "AsyncOAuthSettings",
             default: "AsyncCallbackOptions")
```

The arguments for a failure function.

**Arguments**:

- `request` - The request.
- `reason` - The response.
- `error` - An exception if exists.
- `suggested_status_code` - The recommended HTTP status code for the failure.
- `settings` - The settings for Slack OAuth flow.
- `default` - The default `AsyncCallbackOptions`.

## AsyncCallbackOptions Objects

```python
class AsyncCallbackOptions()
```

#### success: `Callable[[AsyncSuccessArgs], Awaitable[BoltResponse]]`

#### failure: `Callable[[AsyncFailureArgs], Awaitable[BoltResponse]]`

#### \_\_init\_\_

```python
def __init__(success: Callable[[AsyncSuccessArgs], Awaitable[BoltResponse]],
             failure: Callable[[AsyncFailureArgs], Awaitable[BoltResponse]])
```

## DefaultAsyncCallbackOptions Objects

```python
class DefaultAsyncCallbackOptions(AsyncCallbackOptions)
```

#### success: `Callable[[AsyncSuccessArgs], Awaitable[BoltResponse]]`

#### failure: `Callable[[AsyncFailureArgs], Awaitable[BoltResponse]]`

#### \_\_init\_\_

```python
def __init__(*, logger: Logger, state_utils: OAuthStateUtils,
             redirect_uri_page_renderer: RedirectUriPageRenderer)
```

