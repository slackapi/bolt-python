---
sidebar_label: oauth_settings
title: slack_bolt.oauth.oauth_settings
---

## `OAuthSettings`

```python
OAuthSettings(*, client_id=None, client_secret=None, scopes=None, user_scopes=None, redirect_uri=None, install_path='/slack/install', install_page_rendering_enabled=True, redirect_uri_path='/slack/oauth_redirect', callback_options=None, success_url=None, failure_url=None, authorization_url=None, installation_store=None, installation_store_bot_only=False, token_rotation_expiration_minutes=120, user_token_resolution='authed_user', state_validation_enabled=True, state_store=None, state_cookie_name=OAuthStateUtils.default_cookie_name, state_expiration_seconds=OAuthStateUtils.default_expiration_seconds, logger=logging.getLogger(__name__))
```

The settings for Slack App installation (OAuth flow).

**Parameters:**

- **client_id** (Optional[str]) – Check the value in Settings > Basic Information > App Credentials
- **client_secret** (Optional[str]) – Check the value in Settings > Basic Information > App Credentials
- **scopes** (Optional[Union[Sequence[str], str]]) – Check the value in Settings > Manage Distribution
- **user_scopes** (Optional[Union[Sequence[str], str]]) – Check the value in Settings > Manage Distribution
- **redirect_uri** (Optional[str]) – Check the value in Features > OAuth & Permissions > Redirect URLs
- **install_path** (str) – The endpoint to start an OAuth flow (Default: `/slack/install`)
- **install_page_rendering_enabled** (bool) – Renders a web page for install_path access if True
- **redirect_uri_path** (str) – The path of Redirect URL (Default: `/slack/oauth_redirect`)
- **callback_options** (Optional[CallbackOptions]) – Give success/failure functions f you want to customize callback functions.
- **success_url** (Optional[str]) – Set a complete URL if you want to redirect end-users when an installation completes.
- **failure_url** (Optional[str]) – Set a complete URL if you want to redirect end-users when an installation fails.
- **authorization_url** (Optional[str]) – Set a URL if you want to customize the URL `https://slack.com/oauth/v2/authorize`
- **installation_store** (Optional[InstallationStore]) – Specify the instance of `InstallationStore` (Default: `FileInstallationStore`)
- **installation_store_bot_only** (bool) – Use `InstallationStore#find_bot()` if True (Default: False)
- **token_rotation_expiration_minutes** (int) – Minutes before refreshing tokens (Default: 2 hours)
- **user_token_resolution** (str) – The option to pick up a user token per request (Default: authed_user)
The available values are "authed_user" and "actor". When you want to resolve the user token per request
using the event's actor IDs, you can set "actor" instead. With this option, bolt-python tries to resolve
a user token for context.actor_enterprise/team/user_id. This can be useful for events in Slack Connect
channels. Note that actor IDs can be absent in some scenarios.
- **state_validation_enabled** (bool) – Set False if your OAuth flow omits the state parameter validation (Default: True)
- **state_store** (Optional[OAuthStateStore]) – Specify the instance of `InstallationStore` (Default: `FileOAuthStateStore`)
- **state_cookie_name** (str) – The cookie name that is set for installers' browser. (Default: "slack-app-oauth-state")
- **state_expiration_seconds** (int) – The seconds that the state value is alive (Default: 600 seconds)
- **logger** (Logger) – The logger that will be used internally
