---
sidebar_label: async_attaching_conversation_kwargs
title: slack_bolt.middleware.attaching_conversation_kwargs.async_attaching_conversation_kwargs
---

## AsyncAssistantUtilities Objects

```python
class AsyncAssistantUtilities()
```

#### payload: `dict`

#### client: `AsyncWebClient`

#### channel\_id: `str`

#### thread\_ts: `str`

#### thread\_context\_store: `AsyncAssistantThreadContextStore`

#### \_\_init\_\_

```python
def __init__(
        *,
        payload: dict,
        context: AsyncBoltContext,
        thread_context_store: Optional[AsyncAssistantThreadContextStore] = None
)
```

#### set\_title

```python
@property
def set_title() -> AsyncSetTitle
```

#### say

```python
@property
def say() -> AsyncSay
```

#### get\_thread\_context

```python
@property
def get_thread_context() -> AsyncGetThreadContext
```

#### save\_thread\_context

```python
@property
def save_thread_context() -> AsyncSaveThreadContext
```

## AsyncAssistantThreadContextStore Objects

```python
class AsyncAssistantThreadContextStore()
```

#### save

```python
async def save(*, channel_id: str, thread_ts: str, context: Dict[str,
                                                                 str]) -> None
```

#### find

```python
async def find(*, channel_id: str,
               thread_ts: str) -> Optional[AssistantThreadContext]
```

## AsyncSayStream Objects

```python
class AsyncSayStream()
```

#### client: `AsyncWebClient`

#### channel: `Optional[str]`

#### recipient\_team\_id: `Optional[str]`

#### recipient\_user\_id: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(*,
             client: AsyncWebClient,
             channel: Optional[str] = None,
             recipient_team_id: Optional[str] = None,
             recipient_user_id: Optional[str] = None,
             thread_ts: Optional[str] = None)
```

## AsyncSetStatus Objects

```python
class AsyncSetStatus()
```

#### client: `AsyncWebClient`

#### channel\_id: `str`

#### thread\_ts: `str`

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient, channel_id: str, thread_ts: str)
```

## AsyncSetSuggestedPrompts Objects

```python
class AsyncSetSuggestedPrompts()
```

#### client: `AsyncWebClient`

#### channel\_id: `str`

#### thread\_ts: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(client: AsyncWebClient,
             channel_id: str,
             thread_ts: Optional[str] = None)
```

## AsyncMiddleware Objects

```python
class AsyncMiddleware(metaclass=ABCMeta)
```

A middleware can process request data before other middleware and listener functions.

#### async\_process

```python
@abstractmethod
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

```python
    @app.middleware
    async def simple_middleware(req, resp, next):
        # do something here
        await next()
```

This `async_process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
    @app.middleware
    async def simple_middleware(req, resp, next_):
        # do something here
        await next_()
```

**Arguments**:

- `req` - The incoming request
- `resp` - The response
- `next` - The function to tell the chain that it can continue
  

**Returns**:

  Processed response (optional)

#### name

```python
@property
def name() -> str
```

The name of this middleware

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body: `str`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### context: `AsyncBoltContext`

The context in this request.

#### lazy\_only: `bool`

#### lazy\_function\_name: `Optional[str]`

#### mode: `str`

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
def to_copyable() -> "AsyncBoltRequest"
```

#### is\_app\_home\_opened\_event

```python
def is_app_home_opened_event(body: Dict[str, Any],
                             tab: Optional[str] = None) -> bool
```

#### is\_assistant\_event

```python
def is_assistant_event(body: Dict[str, Any]) -> bool
```

#### is\_assistant\_thread\_context\_changed\_event

```python
def is_assistant_thread_context_changed_event(body: Dict[str, Any]) -> bool
```

#### is\_assistant\_thread\_started\_event

```python
def is_assistant_thread_started_event(body: Dict[str, Any]) -> bool
```

#### is\_im\_message\_event

```python
def is_im_message_event(body: Dict[str, Any]) -> bool
```

#### to\_event

```python
def to_event(body: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status: `int`

HTTP status code

#### body: `str`

The response body (dict and str are supported)

#### headers: `Dict[str, Sequence[str]]`

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

## AsyncAttachingConversationKwargs Objects

```python
class AsyncAttachingConversationKwargs(AsyncMiddleware)
```

#### thread\_context\_store: `Optional[AsyncAssistantThreadContextStore]`

#### \_\_init\_\_

```python
def __init__(
        thread_context_store: Optional[AsyncAssistantThreadContextStore] = None
)
```

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

