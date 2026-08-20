---
sidebar_label: oauth_settings
title: slack_bolt.oauth.oauth_settings
---

## OAuthSettings Objects

```python
class OAuthSettings()
```

#### client\_id: `str`

#### client\_secret: `str`

#### scopes: `Optional[Sequence[str]]`

#### user\_scopes: `Optional[Sequence[str]]`

#### redirect\_uri: `Optional[str]`

#### install\_path: `str`

#### install\_page\_rendering\_enabled: `bool`

#### redirect\_uri\_path: `str`

#### callback\_options: `Optional[CallbackOptions]`

#### success\_url: `Optional[str]`

#### failure\_url: `Optional[str]`

#### authorization\_url: `str`

#### installation\_store: `InstallationStore`

#### installation\_store\_bot\_only: `bool`

#### token\_rotation\_expiration\_minutes: `int`

#### authorize: `Authorize`

#### user\_token\_resolution: `str`

#### state\_validation\_enabled: `bool`

#### state\_store: `OAuthStateStore`

#### state\_cookie\_name: `str`

#### state\_expiration\_seconds: `int`

#### state\_utils: `OAuthStateUtils`

#### authorize\_url\_generator: `AuthorizeUrlGenerator`

#### redirect\_uri\_page\_renderer: `RedirectUriPageRenderer`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(
    *,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    scopes: Optional[Union[Sequence[str], str]] = None,
    user_scopes: Optional[Union[Sequence[str], str]] = None,
    redirect_uri: Optional[str] = None,
    install_path: str = '/slack/install',
    install_page_rendering_enabled: bool = True,
    redirect_uri_path: str = '/slack/oauth_redirect',
    callback_options: Optional[CallbackOptions] = None,
    success_url: Optional[str] = None,
    failure_url: Optional[str] = None,
    authorization_url: Optional[str] = None,
    installation_store: Optional[InstallationStore] = None,
    installation_store_bot_only: bool = False,
    token_rotation_expiration_minutes: int = 120,
    user_token_resolution: str = 'authed_user',
    state_validation_enabled: bool = True,
    state_store: Optional[OAuthStateStore] = None,
    state_cookie_name: str = OAuthStateUtils.default_cookie_name,
    state_expiration_seconds: int = OAuthStateUtils.default_expiration_seconds,
    logger: Logger = logging.getLogger(__name__))
```

The settings for Slack App installation (OAuth flow).

**Arguments**:

- `client_id` _Optional[str]_ - Check the value in Settings > Basic Information > App Credentials
- `client_secret` _Optional[str]_ - Check the value in Settings > Basic Information > App Credentials
- `scopes` _Optional[Union[Sequence[str], str]]_ - Check the value in Settings > Manage Distribution
- `user_scopes` _Optional[Union[Sequence[str], str]]_ - Check the value in Settings > Manage Distribution
- `redirect_uri` _Optional[str]_ - Check the value in Features > OAuth & Permissions > Redirect URLs
- `install_path` _str_ - The endpoint to start an OAuth flow (Default: `/slack/install`)
- `install_page_rendering_enabled` _bool_ - Renders a web page for install_path access if True
- `redirect_uri_path` _str_ - The path of Redirect URL (Default: `/slack/oauth_redirect`)
- `callback_options` _Optional[CallbackOptions]_ - Give success/failure functions f you want to customize callback functions.
- `success_url` _Optional[str]_ - Set a complete URL if you want to redirect end-users when an installation completes.
- `failure_url` _Optional[str]_ - Set a complete URL if you want to redirect end-users when an installation fails.
- `authorization_url` _Optional[str]_ - Set a URL if you want to customize the URL `https://slack.com/oauth/v2/authorize`
- `installation_store` _Optional[InstallationStore]_ - Specify the instance of `InstallationStore` (Default: `FileInstallationStore`)
- `installation_store_bot_only` _bool_ - Use `InstallationStore#find_bot()` if True (Default: False)
- `token_rotation_expiration_minutes` _int_ - Minutes before refreshing tokens (Default: 2 hours)
- `user_token_resolution` _str_ - The option to pick up a user token per request (Default: authed_user)
  The available values are "authed_user" and "actor". When you want to resolve the user token per request
  using the event's actor IDs, you can set "actor" instead. With this option, bolt-python tries to resolve
  a user token for context.actor_enterprise/team/user_id. This can be useful for events in Slack Connect
  channels. Note that actor IDs can be absent in some scenarios.
- `state_validation_enabled` _bool_ - Set False if your OAuth flow omits the state parameter validation (Default: True)
- `state_store` _Optional[OAuthStateStore]_ - Specify the instance of `InstallationStore` (Default: `FileOAuthStateStore`)
- `state_cookie_name` _str_ - The cookie name that is set for installers' browser. (Default: "slack-app-oauth-state")
- `state_expiration_seconds` _int_ - The seconds that the state value is alive (Default: 600 seconds)
- `logger` _Logger_ - The logger that will be used internally
