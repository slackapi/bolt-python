---
sidebar_label: async_attaching_conversation_kwargs
title: slack_bolt.middleware.attaching_conversation_kwargs.async_attaching_conversation_kwargs
---

## AsyncAssistantUtilities Objects

```python
class AsyncAssistantUtilities()
```

#### payload

#### client

#### channel\_id

#### thread\_ts

#### thread\_context\_store

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

#### client

#### channel

#### recipient\_team\_id

#### recipient\_user\_id

#### thread\_ts

## AsyncSetStatus Objects

```python
class AsyncSetStatus()
```

#### client

#### channel\_id

#### thread\_ts

## AsyncSetSuggestedPrompts Objects

```python
class AsyncSetSuggestedPrompts()
```

#### client

#### channel\_id

#### thread\_ts

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

## AsyncAttachingConversationKwargs Objects

```python
class AsyncAttachingConversationKwargs(AsyncMiddleware)
```

#### thread\_context\_store

#### async\_process

```python
async def async_process(
        *, req: AsyncBoltRequest, resp: BoltResponse,
        next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

