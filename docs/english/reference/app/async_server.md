---
sidebar_label: async_server
title: slack_bolt.app.async_server
---

#### to\_bolt\_request

```python
async def to_bolt_request(request: web.Request) -> AsyncBoltRequest
```

#### to\_aiohttp\_response

```python
async def to_aiohttp_response(bolt_resp: BoltResponse) -> web.Response
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

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

#### get\_boot\_message

```python
def get_boot_message(development_server: bool = False) -> str
```

## AsyncSlackAppServer Objects

```python
class AsyncSlackAppServer()
```

#### port

#### path

#### host

#### bolt\_app

#### web\_app

#### \_\_init\_\_

```python
def __init__(port: int,
             path: str,
             app: "AsyncApp",
             host: Optional[str] = None)
```

Standalone AIOHTTP Web Server.
Refer to https://docs.aiohttp.org/en/stable/web.html for details of AIOHTTP.

**Arguments**:

- `port` - The port to listen on
- `path` - The path to receive incoming requests from Slack
- `app` - The `AsyncApp` instance that is used for processing requests
- `host` - The hostname to serve the web endpoints. (Default: 0.0.0.0)

#### handle\_get\_requests

```python
async def handle_get_requests(request: web.Request) -> web.Response
```

#### handle\_post\_requests

```python
async def handle_post_requests(request: web.Request) -> web.Response
```

#### start

```python
def start(host: Optional[str] = None) -> None
```

Starts a new web server process.

