---
sidebar_label: attaching_conversation_kwargs
title: slack_bolt.middleware.attaching_conversation_kwargs.attaching_conversation_kwargs
---

## AssistantThreadContextStore Objects

```python
class AssistantThreadContextStore()
```

#### save

```python
def save(*, channel_id: str, thread_ts: str, context: Dict[str, str]) -> None
```

#### find

```python
def find(*, channel_id: str,
         thread_ts: str) -> Optional[AssistantThreadContext]
```

## SayStream Objects

```python
class SayStream()
```

#### client

#### channel

#### recipient\_team\_id

#### recipient\_user\_id

#### thread\_ts

## SetStatus Objects

```python
class SetStatus()
```

#### client

#### channel\_id

#### thread\_ts

## SetSuggestedPrompts Objects

```python
class SetSuggestedPrompts()
```

#### client

#### channel\_id

#### thread\_ts

## Middleware Objects

```python
class Middleware(metaclass=ABCMeta)
```

A middleware can process request data before other middleware and listener functions.

#### process

```python
@abstractmethod
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

```python
    @app.middleware
    def simple_middleware(req, resp, next):
        # do something here
        next()
```

This `process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
    @app.middleware
    def simple_middleware(req, resp, next_):
        # do something here
        next_()
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

## AssistantUtilities Objects

```python
class AssistantUtilities()
```

#### payload

#### client

#### channel\_id

#### thread\_ts

#### thread\_context\_store

#### set\_title

```python
@property
def set_title() -> SetTitle
```

#### say

```python
@property
def say() -> Say
```

#### get\_thread\_context

```python
@property
def get_thread_context() -> GetThreadContext
```

#### save\_thread\_context

```python
@property
def save_thread_context() -> SaveThreadContext
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

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body

#### query

#### headers

#### content\_type

#### body

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
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

## AttachingConversationKwargs Objects

```python
class AttachingConversationKwargs(Middleware)
```

#### thread\_context\_store

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

