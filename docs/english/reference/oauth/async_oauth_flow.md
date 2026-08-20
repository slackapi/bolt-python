---
sidebar_label: async_oauth_flow
title: slack_bolt.oauth.async_oauth_flow
---

## AsyncOAuthFlow Objects

```python
class AsyncOAuthFlow()
```

#### settings: `AsyncOAuthSettings`

#### client\_id: `str`

#### redirect\_uri: `Optional[str]`

#### install\_path: `str`

#### redirect\_uri\_path: `str`

#### success\_handler: `Callable[[AsyncSuccessArgs], Awaitable[BoltResponse]]`

#### failure\_handler: `Callable[[AsyncFailureArgs], Awaitable[BoltResponse]]`

#### \_\_init\_\_

```python
def __init__(
    *,
    client: Optional[AsyncWebClient] = None,
    logger: Optional[Logger] = None,
    settings: AsyncOAuthSettings)
```

The module to run the Slack app installation flow (OAuth flow).

**Arguments**:

- `client` _Optional[AsyncWebClient]_ - The `slack_sdk.web.async_client.AsyncWebClient` instance.
- `logger` _Optional[Logger]_ - The logger.
- `settings` _AsyncOAuthSettings_ - OAuth settings to configure this module.

#### client

```python
@property
def client() -> AsyncWebClient
```

#### logger

```python
@property
def logger() -> Logger
```

#### sqlite3

```python
def sqlite3(
    database: str,
    authorization_url: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    scopes: Optional[Sequence[str]] = None,
    user_scopes: Optional[Sequence[str]] = None,
    redirect_uri: Optional[str] = None,
    install_path: Optional[str] = None,
    redirect_uri_path: Optional[str] = None,
    callback_options: Optional[AsyncCallbackOptions] = None,
    success_url: Optional[str] = None,
    failure_url: Optional[str] = None,
    state_cookie_name: str = OAuthStateUtils.default_cookie_name,
    state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
    installation_store_bot_only: bool = False,
    client: Optional[AsyncWebClient] = None,
    logger: Optional[Logger] = None) -> AsyncOAuthFlow
```

#### handle\_installation

```python
async def handle_installation(request: AsyncBoltRequest) -> BoltResponse
```

#### issue\_new\_state

```python
async def issue_new_state(request: AsyncBoltRequest) -> str
```

#### build\_authorize\_url

```python
async def build_authorize_url(state: str, request: AsyncBoltRequest) -> str
```

#### build\_install\_page\_html

```python
async def build_install_page_html(url: str, request: AsyncBoltRequest) -> str
```

#### append\_set\_cookie\_headers

```python
async def append_set_cookie_headers(headers: dict, set_cookie_value: Optional[str])
```

#### handle\_callback

```python
async def handle_callback(request: AsyncBoltRequest) -> BoltResponse
```

#### run\_installation

```python
async def run_installation(code: str) -> Optional[Installation]
```

#### store\_installation

```python
async def store_installation(request: AsyncBoltRequest, installation: Installation)
```
