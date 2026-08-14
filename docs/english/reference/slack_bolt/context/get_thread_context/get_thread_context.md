---
sidebar_label: get_thread_context
title: slack_bolt.context.get_thread_context.get_thread_context
---

## AssistantThreadContext Objects

```python
class AssistantThreadContext(dict)
```

#### enterprise\_id

#### team\_id

#### channel\_id

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

#### thread\_context\_store

#### payload

#### channel\_id

#### thread\_ts

#### thread\_context\_loaded

#### \_\_init\_\_

```python
def __init__(thread_context_store: AssistantThreadContextStore,
             channel_id: str, thread_ts: str, payload: dict)
```

