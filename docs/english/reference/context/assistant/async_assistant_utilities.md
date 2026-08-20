---
sidebar_label: async_assistant_utilities
title: slack_bolt.context.assistant.async_assistant_utilities
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
    thread_context_store: Optional[AsyncAssistantThreadContextStore] = None)
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
