---
sidebar_label: oauth_flow
title: slack_bolt.oauth.oauth_flow
---

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

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

## DefaultCallbackOptions Objects

```python
class DefaultCallbackOptions(CallbackOptions)
```

#### success

#### failure

#### \_\_init\_\_

```python
def __init__(*, logger: Logger, state_utils: OAuthStateUtils,
             redirect_uri_page_renderer: RedirectUriPageRenderer)
```

## CallbackOptions Objects

```python
class CallbackOptions()
```

#### success

A handler for successful installation.

#### failure

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

## OAuthSettings Objects

```python
class OAuthSettings()
```

#### client\_id

Check the value in Settings &gt; Basic Information &gt; App Credentials

#### client\_secret

Check the value in Settings &gt; Basic Information &gt; App Credentials

#### scopes

Check the value in Settings &gt; Manage Distribution

#### user\_scopes

Check the value in Settings &gt; Manage Distribution

#### redirect\_uri

Check the value in Features &gt; OAuth &amp; Permissions &gt; Redirect URLs

#### install\_path

The endpoint to start an OAuth flow (Default: `/slack/install`)

#### install\_page\_rendering\_enabled

Renders a web page for install_path access if True

#### redirect\_uri\_path

The path of Redirect URL (Default: `/slack/oauth_redirect`)

#### callback\_options

Give success/failure functions f you want to customize callback functions.

#### success\_url

Set a complete URL if you want to redirect end-users when an installation completes.

#### failure\_url

Set a complete URL if you want to redirect end-users when an installation fails.

#### authorization\_url

Set a URL if you want to customize the URL `https://slack.com/oauth/v2/authorize`

#### installation\_store

Specify the instance of `InstallationStore` (Default: `FileInstallationStore`)

#### installation\_store\_bot\_only

Use `InstallationStore#find_bot()` if True (Default: False)

#### token\_rotation\_expiration\_minutes

Minutes before refreshing tokens (Default: 2 hours)

#### authorize

#### user\_token\_resolution

The option to pick up a user token per request (Default: authed_user)
The available values are &quot;authed_user&quot; and &quot;actor&quot;. When you want to resolve the user token
per request using the event&#x27;s actor IDs, you can set &quot;actor&quot; instead. With this option,
bolt-python tries to resolve a user token for context.actor_enterprise/team/user_id.
This can be useful for events in Slack Connect channels. Note that actor IDs can be absent
in some scenarios.

#### state\_validation\_enabled

Set False if your OAuth flow omits the state parameter validation (Default: True)

#### state\_store

Specify the instance of `InstallationStore` (Default: `FileOAuthStateStore`)

#### state\_cookie\_name

The cookie name that is set for installers&#x27; browser. (Default: &quot;slack-app-oauth-state&quot;)

#### state\_expiration\_seconds

The seconds that the state value is alive (Default: 600 seconds)

#### state\_utils

#### authorize\_url\_generator

#### redirect\_uri\_page\_renderer

#### logger

The logger that will be used internally

#### \_\_init\_\_

```python
def __init__(
    *,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    scopes: Optional[Union[Sequence[str], str]] = None,
    user_scopes: Optional[Union[Sequence[str], str]] = None,
    redirect_uri: Optional[str] = None,
    install_path: str = "/slack/install",
    install_page_rendering_enabled: bool = True,
    redirect_uri_path: str = "/slack/oauth_redirect",
    callback_options: Optional[CallbackOptions] = None,
    success_url: Optional[str] = None,
    failure_url: Optional[str] = None,
    authorization_url: Optional[str] = None,
    installation_store: Optional[InstallationStore] = None,
    installation_store_bot_only: bool = False,
    token_rotation_expiration_minutes: int = 120,
    user_token_resolution: str = "authed_user",
    state_validation_enabled: bool = True,
    state_store: Optional[OAuthStateStore] = None,
    state_cookie_name: str = OAuthStateUtils.default_cookie_name,
    state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
    logger: Logger = logging.getLogger(__name__))
```

The settings for Slack App installation (OAuth flow).

**Arguments**:

- `client_id` - Check the value in Settings &gt; Basic Information &gt; App Credentials
- `client_secret` - Check the value in Settings &gt; Basic Information &gt; App Credentials
- `scopes` - Check the value in Settings &gt; Manage Distribution
- `user_scopes` - Check the value in Settings &gt; Manage Distribution
- `redirect_uri` - Check the value in Features &gt; OAuth &amp; Permissions &gt; Redirect URLs
- `install_path` - The endpoint to start an OAuth flow (Default: `/slack/install`)
- `install_page_rendering_enabled` - Renders a web page for install_path access if True
- `redirect_uri_path` - The path of Redirect URL (Default: `/slack/oauth_redirect`)
- `callback_options` - Give success/failure functions f you want to customize callback functions.
- `success_url` - Set a complete URL if you want to redirect end-users when an installation completes.
- `failure_url` - Set a complete URL if you want to redirect end-users when an installation fails.
- `authorization_url` - Set a URL if you want to customize the URL `https://slack.com/oauth/v2/authorize`
- `installation_store` - Specify the instance of `InstallationStore` (Default: `FileInstallationStore`)
- `installation_store_bot_only` - Use `InstallationStore#find_bot()` if True (Default: False)
- `token_rotation_expiration_minutes` - Minutes before refreshing tokens (Default: 2 hours)
- `user_token_resolution` - The option to pick up a user token per request (Default: authed_user)
  The available values are &quot;authed_user&quot; and &quot;actor&quot;. When you want to resolve the user token per request
  using the event&#x27;s actor IDs, you can set &quot;actor&quot; instead. With this option, bolt-python tries to resolve
  a user token for context.actor_enterprise/team/user_id. This can be useful for events in Slack Connect
  channels. Note that actor IDs can be absent in some scenarios.
- `state_validation_enabled` - Set False if your OAuth flow omits the state parameter validation (Default: True)
- `state_store` - Specify the instance of `InstallationStore` (Default: `FileOAuthStateStore`)
- `state_cookie_name` - The cookie name that is set for installers&#x27; browser. (Default: &quot;slack-app-oauth-state&quot;)
- `state_expiration_seconds` - The seconds that the state value is alive (Default: 600 seconds)
- `logger` - The logger that will be used internally

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

#### create\_web\_client

```python
def create_web_client(token: Optional[str] = None,
                      logger: Optional[Logger] = None) -> WebClient
```

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

