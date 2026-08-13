---
sidebar_label: async_oauth_flow
title: slack_bolt.oauth.async_oauth_flow
---

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

#### error\_oauth\_settings\_invalid\_type\_async

```python
def error_oauth_settings_invalid_type_async() -> str
```

## AsyncCallbackOptions Objects

```python
class AsyncCallbackOptions()
```

#### success

#### failure

## DefaultAsyncCallbackOptions Objects

```python
class DefaultAsyncCallbackOptions(AsyncCallbackOptions)
```

#### success

#### failure

## AsyncSuccessArgs Objects

```python
class AsyncSuccessArgs()
```

## AsyncFailureArgs Objects

```python
class AsyncFailureArgs()
```

## AsyncOAuthSettings Objects

```python
class AsyncOAuthSettings()
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

#### user\_token\_resolution

#### authorize

#### state\_validation\_enabled

#### state\_store

#### state\_cookie\_name

#### state\_expiration\_seconds

#### state\_utils

#### authorize\_url\_generator

#### redirect\_uri\_page\_renderer

#### logger

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body

#### body

#### query

#### headers

#### content\_type

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### to\_copyable

```python
def to_copyable() -> "AsyncBoltRequest"
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

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

#### create\_async\_web\_client

```python
def create_async_web_client(token: Optional[str] = None,
                            logger: Optional[Logger] = None) -> AsyncWebClient
```

## AsyncOAuthFlow Objects

```python
class AsyncOAuthFlow()
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
def client() -> AsyncWebClient
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
            state_expiration_seconds: int = OAuthStateUtils.
            default_expiration_seconds,
            installation_store_bot_only: bool = False,
            client: Optional[AsyncWebClient] = None,
            logger: Optional[Logger] = None) -> "AsyncOAuthFlow"
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
async def append_set_cookie_headers(headers: dict,
                                    set_cookie_value: Optional[str])
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
async def store_installation(request: AsyncBoltRequest,
                             installation: Installation)
```

