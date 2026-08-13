---
sidebar_label: listener_matcher
title: slack_bolt.listener_matcher
---

A listener matcher is a simplified version of listener middleware.
A listener matcher function returns bool value instead of `next()` method invocation inside.
This interface enables developers to utilize simple predicate functions for additional listener conditions.

## CustomListenerMatcher Objects

```python
class CustomListenerMatcher(ListenerMatcher)
```

#### app\_name

#### func

#### arg\_names

#### logger

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

