---
sidebar_label: assistant
title: slack_bolt.middleware.assistant.assistant
slug: assistant
---

## Assistant Objects

```python
class Assistant(Middleware)
```

#### thread\_context\_store: `Optional[AssistantThreadContextStore]`

#### base\_logger: `Optional[logging.Logger]`

#### \_\_init\_\_

```python
def __init__(
    *,
    app_name: str = 'assistant',
    thread_context_store: Optional[AssistantThreadContextStore] = None,
    logger: Optional[logging.Logger] = None)
```

#### thread\_started

```python
def thread_started(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### user\_message

```python
def user_message(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### bot\_message

```python
def bot_message(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### thread\_context\_changed

```python
def thread_context_changed(
    *args,
    matchers: Optional[Union[Callable[..., bool], ListenerMatcher]] = None,
    middleware: Optional[Union[Callable, Middleware]] = None,
    lazy: Optional[List[Callable[..., None]]] = None)
```

#### default\_thread\_context\_changed

```python
def default_thread_context_changed(
    save_thread_context: SaveThreadContext,
    payload: dict)
```

#### process

```python
def process(
    *,
    req: BoltRequest,
    resp: BoltResponse,
    next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

#### build\_listener

```python
def build_listener(
    listener_or_functions: Union[Listener, Callable, List[Callable]],
    matchers: Optional[List[Union[ListenerMatcher, Callable[..., bool]]]] = None,
    middleware: Optional[List[Middleware]] = None,
    base_logger: Optional[Logger] = None) -> Listener
```
