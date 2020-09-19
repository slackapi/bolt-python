---
title: Authenticating with OAuth
lang: en
slug: authenticating-oauth
order: 14
---

<div class="section-content">

Slack apps installed on multiple workspaces will need to implement OAuth, then store installation information (like access tokens) securely. By providing `client_id`, `client_secret`, `scopes`, `installation_store`, and `state_store` when initializing App, Bolt for Python will handle the work of setting up OAuth routes and verifying state. If you’re implementing a custom receiver, you can make use of our [OAuth library](https://slack.dev/python-slack-sdk/oauth), which is what Bolt for Python uses under the hood.

Bolt for Python will create a **Redirect URL** `slack/oauth_redirect`, which Slack uses to redirect users after they complete your app’s installation flow. You will need to add this **Redirect URL** in your app configuration settings under **OAuth and Permissions**. This path can be configured in the `OAuthSettings` argument described below.

Bolt for Python will also create a `slack/install` route, where you can find an **Add to Slack** button for your app to perform direct installs of your app. If you need any additional authorizations (user tokens) from users inside a team when your app is already installed or a reason to dynamically generate an install URL, you can pass your own custom URL generator to `oauth_settings` as `authorize_url_generator`.

To learn more about the OAuth installation flow with Slack, [read the API documentation](https://api.slack.com/authentication/oauth-v2).

</div>

```python
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

oauth_settings = OAuthSettings(
    client_id=os.environ["SLACK_CLIENT_ID"],
    client_secret=os.environ["SLACK_CLIENT_SECRET"],
    scopes=["channels:read", "groups:read", "chat:write"],
    installation_store=FileInstallationStore(),
    state_store=FileOAuthStateStore(expiration_seconds=120)
)

app = App(signing_secret=os.environ["SIGNING_SECRET"],
          oauth_settings=oauth_settings)
```

<details class="secondary-wrapper">
<summary class="section-head" markdown="0">
<h4 class="section-head">Customizing OAuth defaults</h4>
</summary>

<div class="secondary-content" markdown="0">
You can override the default OAuth using `oauth_settings`, which can be passed in during the initialization of App. You can override the following:

- `install_path`: Override default path for "Add to Slack" button
- `redirect_uri`: Override default redirect url path
- `callback_options`: Provide custom success and failure pages at the end of the OAuth flow
- `state_store`: Provide a custom state store instead of using the built in `FileOAuthStateStore`
- `installation_store`: Provide a custom installation store instead of the built-in `FileInstallationStore`

</div>

```python
app = App(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    installation_store=FileInstallationStore(),
    oauth_settings=OAuthSettings(
        client_id=os.environ.get("SLACK_CLIENT_ID"),
        client_secret=os.environ.get("SLACK_CLIENT_SECRET"),
        scopes=["app_mentions:read", "channels:history", "im:history", "chat:write"],
        user_scopes=[],
        redirect_uri=None,
        install_path="/slack/install",
        redirect_uri_path="/slack/oauth_redirect",
        state_store=FileOAuthStateStore(expiration_seconds=600),
        callback_options=CallbackOptions(success=success,
                                         failure=failure),
    ),
)
```

</details>
