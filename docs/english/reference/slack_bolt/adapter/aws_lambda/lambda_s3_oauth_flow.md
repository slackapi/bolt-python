---
sidebar_label: lambda_s3_oauth_flow
title: slack_bolt.adapter.aws_lambda.lambda_s3_oauth_flow
---

## InstallationStoreAuthorize Objects

```python
class InstallationStoreAuthorize(Authorize)
```

If you use the OAuth flow settings, this `authorize` implementation will be used.
As long as your own InstallationStore (or the built-in ones) works as you expect,
you can expect that the `authorize` layer should work for you without any customization.

#### authorize\_result\_cache

#### bot\_only

#### user\_token\_resolution

#### find\_installation\_available

#### find\_bot\_available

#### token\_rotator

## OAuthFlow Objects

```python
class OAuthFlow()
```

#### settings

#### client\_id

#### redirect\_uri

#### install\_path

#### redirect\_uri\_path

#### success\_handler

#### failure\_handler

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

## OAuthSettings Objects

```python
class OAuthSettings()
```

#### client\_id

#### client\_secret

#### scopes

#### user\_scopes

#### redirect\_uri

#### install\_path

#### install\_page\_rendering\_enabled

#### redirect\_uri\_path

#### callback\_options

#### success\_url

#### failure\_url

#### authorization\_url

default: https://slack.com/oauth/v2/authorize

#### installation\_store

#### installation\_store\_bot\_only

#### token\_rotation\_expiration\_minutes

#### authorize

#### user\_token\_resolution

default: &quot;authed_user&quot;

#### state\_validation\_enabled

#### state\_store

#### state\_cookie\_name

#### state\_expiration\_seconds

#### state\_utils

#### authorize\_url\_generator

#### redirect\_uri\_page\_renderer

#### logger

#### create\_web\_client

```python
def create_web_client(token: Optional[str] = None,
                      logger: Optional[Logger] = None) -> WebClient
```

## LambdaS3OAuthFlow Objects

```python
class LambdaS3OAuthFlow(OAuthFlow)
```

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

