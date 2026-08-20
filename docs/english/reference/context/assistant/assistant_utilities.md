---
sidebar_label: assistant_utilities
title: slack_bolt.context.assistant.assistant_utilities
---

## AssistantUtilities Objects

```python
class AssistantUtilities()
```

#### payload: `dict`

#### client: `WebClient`

#### channel\_id: `str`

#### thread\_ts: `str`

#### thread\_context\_store: `AssistantThreadContextStore`

#### \_\_init\_\_

```python
def __init__(
    *,
    payload: dict,
    context: BoltContext,
    thread_context_store: Optional[AssistantThreadContextStore] = None)
```

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
