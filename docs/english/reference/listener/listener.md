---
sidebar_label: listener
title: slack_bolt.listener.listener
slug: listener
---

## Listener Objects

```python
class Listener()
```

#### matchers: `Sequence[ListenerMatcher]`

#### middleware: `Sequence[Middleware]`

#### ack\_function: `Callable[..., BoltResponse]`

#### lazy\_functions: `Sequence[Callable[..., None]]`

#### auto\_acknowledgement: `bool`

#### ack\_timeout: `int`

#### matches

```python
def matches(*, req: BoltRequest, resp: BoltResponse) -> bool
```

#### run\_middleware

```python
def run_middleware(
    *,
    req: BoltRequest,
    resp: BoltResponse) -> Tuple[Optional[BoltResponse], bool]
```

Runs a middleware.

**Arguments**:

- `req` _BoltRequest_ - The incoming request
- `resp` _BoltResponse_ - The current response

**Returns**:

- `Tuple[Optional[BoltResponse], bool]` - A tuple of the processed response and a flag indicating termination

#### run\_ack\_function

```python
def run_ack_function(
    *,
    request: BoltRequest,
    response: BoltResponse) -> Optional[BoltResponse]
```

Runs all the registered middleware and then run the listener function.

**Arguments**:

- `request` _BoltRequest_ - The incoming request
- `response` _BoltResponse_ - The current response

**Returns**:

- `Optional[BoltResponse]` - The processed response
