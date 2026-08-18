---
sidebar_label: internals
title: slack_bolt.oauth.internals
---

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body

#### query

The query string data in any data format.

#### headers

The request headers.

#### content\_type

#### body

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### context

The context in this request.

#### lazy\_only

#### lazy\_function\_name

#### mode

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

#### status

HTTP status code

#### body

The response body (dict and str are supported)

#### headers

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

#### warning\_installation\_store\_conflicts

```python
def warning_installation_store_conflicts() -> str
```

## CallbackResponseBuilder Objects

```python
class CallbackResponseBuilder()
```

#### \_\_init\_\_

```python
def __init__(*, logger: Logger, state_utils: OAuthStateUtils,
             redirect_uri_page_renderer: RedirectUriPageRenderer)
```

#### default\_installation\_stores

#### get\_or\_create\_default\_installation\_store

```python
def get_or_create_default_installation_store(
        client_id: str) -> InstallationStore
```

#### select\_consistent\_installation\_store

```python
def select_consistent_installation_store(
        client_id: str, app_store: Optional[InstallationStore],
        oauth_flow_store: Optional[InstallationStore],
        logger: Logger) -> Optional[InstallationStore]
```

#### build\_detailed\_error

```python
def build_detailed_error(reason: str) -> str
```

