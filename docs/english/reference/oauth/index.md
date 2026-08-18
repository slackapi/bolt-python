---
sidebar_label: oauth
title: slack_bolt.oauth
---


Slack OAuth flow support for building an app that is installable in any workspaces.

Refer to https://docs.slack.dev/tools/bolt-python/concepts/authenticating-oauth for details.

## Submodules

- [slack_bolt.oauth.async_callback_options](/tools/bolt-python/reference/oauth/async_callback_options)
- [slack_bolt.oauth.async_internals](/tools/bolt-python/reference/oauth/async_internals)
- [slack_bolt.oauth.async_oauth_flow](/tools/bolt-python/reference/oauth/async_oauth_flow)
- [slack_bolt.oauth.async_oauth_settings](/tools/bolt-python/reference/oauth/async_oauth_settings)
- [slack_bolt.oauth.callback_options](/tools/bolt-python/reference/oauth/callback_options)
- [slack_bolt.oauth.internals](/tools/bolt-python/reference/oauth/internals)
- [slack_bolt.oauth.oauth_flow](/tools/bolt-python/reference/oauth/oauth_flow)
- [slack_bolt.oauth.oauth_settings](/tools/bolt-python/reference/oauth/oauth_settings)

## OAuthFlow Objects

```python
class OAuthFlow()
```

#### settings

OAuth settings to configure this module.

#### client\_id

#### redirect\_uri

#### install\_path

#### redirect\_uri\_path

#### success\_handler

#### failure\_handler

#### \_\_init\_\_

```python
def __init__(*,
             client: Optional[WebClient] = None,
             logger: Optional[Logger] = None,
             settings: OAuthSettings)
```

The module to run the Slack app installation flow (OAuth flow).

**Arguments**:

- `client` - The `slack_sdk.web.WebClient` instance.
- `logger` - The logger.
- `settings` - OAuth settings to configure this module.

#### client

```python
@property
def client() -> WebClient
```

#### logger

```python
@property
def logger() -> Logger
```

#### sqlite3

```python
@classmethod
def sqlite3(cls,
            database: str,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            user_scopes: Optional[Sequence[str]] = None,
            redirect_uri: Optional[str] = None,
            install_path: Optional[str] = None,
            redirect_uri_path: Optional[str] = None,
            callback_options: Optional[CallbackOptions] = None,
            success_url: Optional[str] = None,
            failure_url: Optional[str] = None,
            authorization_url: Optional[str] = None,
            state_cookie_name: str = OAuthStateUtils.default_cookie_name,
            state_expiration_seconds: int = OAuthStateUtils.
            default_expiration_seconds,
            installation_store_bot_only: bool = False,
            token_rotation_expiration_minutes: int = 120,
            client: Optional[WebClient] = None,
            logger: Optional[Logger] = None) -> "OAuthFlow"
```

#### handle\_installation

```python
def handle_installation(request: BoltRequest) -> BoltResponse
```

#### issue\_new\_state

```python
def issue_new_state(request: BoltRequest) -> str
```

#### build\_authorize\_url

```python
def build_authorize_url(state: str, request: BoltRequest) -> str
```

#### build\_install\_page\_html

```python
def build_install_page_html(url: str, request: BoltRequest) -> str
```

#### append\_set\_cookie\_headers

```python
def append_set_cookie_headers(headers: dict, set_cookie_value: Optional[str])
```

#### handle\_callback

```python
def handle_callback(request: BoltRequest) -> BoltResponse
```

#### run\_installation

```python
def run_installation(code: str) -> Optional[Installation]
```

#### store\_installation

```python
def store_installation(request: BoltRequest, installation: Installation)
```

