---
sidebar_label: get_thread_context
title: slack_bolt.context.get_thread_context.get_thread_context
slug: get_thread_context
---

## AssistantThreadContext Objects

```python
class AssistantThreadContext(dict)
```

#### enterprise\_id: `Optional[str]`

#### team\_id: `Optional[str]`

#### channel\_id: `str`

#### \_\_init\_\_

```python
def __init__(payload: dict)
```

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

## GetThreadContext Objects

```python
class GetThreadContext()
```

#### thread\_context\_store: `AssistantThreadContextStore`

#### payload: `dict`

#### channel\_id: `str`

#### thread\_ts: `str`

#### thread\_context\_loaded: `bool`

#### \_\_init\_\_

```python
def __init__(thread_context_store: AssistantThreadContextStore,
             channel_id: str, thread_ts: str, payload: dict)
```

