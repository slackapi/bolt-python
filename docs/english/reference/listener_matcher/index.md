---
sidebar_label: listener_matcher
title: slack_bolt.listener_matcher
---


A listener matcher is a simplified version of listener middleware.
A listener matcher function returns bool value instead of `next()` method invocation inside.
This interface enables developers to utilize simple predicate functions for additional listener conditions.

## Submodules

- [slack_bolt.listener_matcher.async_builtins](/tools/bolt-python/reference/listener_matcher/async_builtins)
- [slack_bolt.listener_matcher.async_listener_matcher](/tools/bolt-python/reference/listener_matcher/async_listener_matcher)
- [slack_bolt.listener_matcher.builtins](/tools/bolt-python/reference/listener_matcher/builtins)
- [slack_bolt.listener_matcher.custom_listener_matcher](/tools/bolt-python/reference/listener_matcher/custom_listener_matcher)
- [slack_bolt.listener_matcher.listener_matcher](/tools/bolt-python/reference/listener_matcher/listener_matcher)

## CustomListenerMatcher Objects

```python
class CustomListenerMatcher(ListenerMatcher)
```

#### app\_name: `str`

#### func: `Callable[..., bool]`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             func: Callable[..., bool],
             base_logger: Optional[Logger] = None)
```

#### matches

```python
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

## ListenerMatcher Objects

```python
class ListenerMatcher(metaclass=ABCMeta)
```

#### matches

```python
@abstractmethod
def matches(req: BoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` - The request
- `resp` - The response
  

**Returns**:

  True if matched.

#### builtin\_listener\_matcher\_classes

