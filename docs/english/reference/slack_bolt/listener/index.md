---
sidebar_label: listener
title: slack_bolt.listener
---

Listeners process an incoming request from Slack if the request&#x27;s type or data structure matches
the predefined conditions of the listener. Typically, a listener acknowledge requests from Slack,
process the request data, and may send response back to Slack.

## CustomListener Objects

```python
class CustomListener(Listener)
```

#### app\_name

#### ack\_function

type: ignore[assignment]

#### lazy\_functions

#### matchers

#### middleware

#### auto\_acknowledgement

#### ack\_timeout

#### arg\_names

#### logger

#### run\_ack\_function

```python
def run_ack_function(*, request: BoltRequest,
                     response: BoltResponse) -> Optional[BoltResponse]
```

## Listener Objects

```python
class Listener(metaclass=ABCMeta)
```

#### matchers

#### middleware

#### ack\_function

#### lazy\_functions

#### auto\_acknowledgement

#### ack\_timeout

#### matches

```python
def matches(*, req: BoltRequest, resp: BoltResponse) -> bool
```

#### run\_middleware

```python
def run_middleware(*, req: BoltRequest,
                   resp: BoltResponse) -> Tuple[Optional[BoltResponse], bool]
```

Runs a middleware.

**Arguments**:

- `req` - The incoming request
- `resp` - The current response
  

**Returns**:

  A tuple of the processed response and a flag indicating termination

#### run\_ack\_function

```python
@abstractmethod
def run_ack_function(*, request: BoltRequest,
                     response: BoltResponse) -> Optional[BoltResponse]
```

Runs all the registered middleware and then run the listener function.

**Arguments**:

- `request` - The incoming request
- `response` - The current response
  

**Returns**:

  The processed response

#### builtin\_listener\_classes

