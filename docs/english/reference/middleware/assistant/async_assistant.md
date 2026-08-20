---
sidebar_label: async_assistant
title: slack_bolt.middleware.assistant.async_assistant
---

## AsyncAssistant Objects

```python
class AsyncAssistant(AsyncMiddleware)
```

#### thread\_context\_store: `Optional[AsyncAssistantThreadContextStore]`

#### base\_logger: `Optional[logging.Logger]`

#### \_\_init\_\_

```python
def __init__(
    *,
    app_name: str = 'assistant',
    thread_context_store: Optional[AsyncAssistantThreadContextStore] = None,
    logger: Optional[logging.Logger] = None)
```

#### thread\_started

```python
def thread_started(
    *args,
    matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]] = None,
    middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### user\_message

```python
def user_message(
    *args,
    matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]] = None,
    middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### bot\_message

```python
def bot_message(
    *args,
    matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]] = None,
    middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### thread\_context\_changed

```python
def thread_context_changed(
    *args,
    matchers: Optional[Union[Callable[..., bool], AsyncListenerMatcher]] = None,
    middleware: Optional[Union[Callable, AsyncMiddleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### default\_thread\_context\_changed

```python
async def default_thread_context_changed(
    save_thread_context: AsyncSaveThreadContext,
    payload: dict)
```

#### async\_process

```python
async def async_process(
    *,
    req: AsyncBoltRequest,
    resp: BoltResponse,
    next: Callable[[], Awaitable[BoltResponse]]) -> Optional[BoltResponse]
```

#### build\_listener

```python
def build_listener(
    listener_or_functions: Union[AsyncListener, Callable, List[Callable]],
    matchers: Optional[List[Union[AsyncListenerMatcher, Callable[..., Awaitable[bool]]]]] = None,
    middleware: Optional[List[AsyncMiddleware]] = None,
    base_logger: Optional[Logger] = None) -> AsyncListener
```
