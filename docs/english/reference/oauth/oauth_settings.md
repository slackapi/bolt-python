---
sidebar_label: oauth_settings
title: slack_bolt.oauth.oauth_settings
---

## Authorize Objects

```python
class Authorize()
```

This provides authorize function that returns AuthorizeResult
for an incoming request from Slack.

#### \_\_init\_\_

```python
def __init__()
```

## InstallationStoreAuthorize Objects

```python
class InstallationStoreAuthorize(Authorize)
```

If you use the OAuth flow settings, this `authorize` implementation will be used.
As long as your own InstallationStore (or the built-in ones) works as you expect,
you can expect that the `authorize` layer should work for you without any customization.

#### authorize\_result\_cache: `Dict[str, AuthorizeResult]`

#### bot\_only: `bool`

#### user\_token\_resolution: `str`

#### find\_installation\_available: `bool`

#### find\_bot\_available: `bool`

#### token\_rotator: `Optional[TokenRotator]`

#### \_\_init\_\_

```python
def __init__(*,
             logger: Logger,
             installation_store: InstallationStore,
             client_id: Optional[str] = None,
             client_secret: Optional[str] = None,
             token_rotation_expiration_minutes: Optional[int] = None,
             bot_only: bool = False,
             cache_enabled: bool = False,
             client: Optional[WebClient] = None,
             user_token_resolution: str = "authed_user")
```

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

#### get\_or\_create\_default\_installation\_store

```python
def get_or_create_default_installation_store(
        client_id: str) -> InstallationStore
```

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

## OAuthSettings Objects

```python
class OAuthSettings()
```

#### client\_id: `str`

Check the value in Settings &gt; Basic Information &gt; App Credentials

#### client\_secret: `str`

Check the value in Settings &gt; Basic Information &gt; App Credentials

#### scopes: `Optional[Sequence[str]]`

Check the value in Settings &gt; Manage Distribution

#### user\_scopes: `Optional[Sequence[str]]`

Check the value in Settings &gt; Manage Distribution

#### redirect\_uri: `Optional[str]`

Check the value in Features &gt; OAuth &amp; Permissions &gt; Redirect URLs

#### install\_path: `str`

The endpoint to start an OAuth flow (Default: `/slack/install`)

#### install\_page\_rendering\_enabled: `bool`

Renders a web page for install_path access if True

#### redirect\_uri\_path: `str`

The path of Redirect URL (Default: `/slack/oauth_redirect`)

#### callback\_options: `Optional[CallbackOptions]`

Give success/failure functions f you want to customize callback functions.

#### success\_url: `Optional[str]`

Set a complete URL if you want to redirect end-users when an installation completes.

#### failure\_url: `Optional[str]`

Set a complete URL if you want to redirect end-users when an installation fails.

#### authorization\_url: `str`

Set a URL if you want to customize the URL `https://slack.com/oauth/v2/authorize`

#### installation\_store: `InstallationStore`

Specify the instance of `InstallationStore` (Default: `FileInstallationStore`)

#### installation\_store\_bot\_only: `bool`

Use `InstallationStore#find_bot()` if True (Default: False)

#### token\_rotation\_expiration\_minutes: `int`

Minutes before refreshing tokens (Default: 2 hours)

#### authorize: `Authorize`

#### user\_token\_resolution: `str`

The option to pick up a user token per request (Default: authed_user)
The available values are &quot;authed_user&quot; and &quot;actor&quot;. When you want to resolve the user token
per request using the event&#x27;s actor IDs, you can set &quot;actor&quot; instead. With this option,
bolt-python tries to resolve a user token for context.actor_enterprise/team/user_id.
This can be useful for events in Slack Connect channels. Note that actor IDs can be absent
in some scenarios.

#### state\_validation\_enabled: `bool`

Set False if your OAuth flow omits the state parameter validation (Default: True)

#### state\_store: `OAuthStateStore`

Specify the instance of `InstallationStore` (Default: `FileOAuthStateStore`)

#### state\_cookie\_name: `str`

The cookie name that is set for installers&#x27; browser. (Default: &quot;slack-app-oauth-state&quot;)

#### state\_expiration\_seconds: `int`

The seconds that the state value is alive (Default: 600 seconds)

#### state\_utils: `OAuthStateUtils`

#### authorize\_url\_generator: `AuthorizeUrlGenerator`

#### redirect\_uri\_page\_renderer: `RedirectUriPageRenderer`

#### logger: `Logger`

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

