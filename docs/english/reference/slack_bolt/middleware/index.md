---
sidebar_label: middleware
title: slack_bolt.middleware
---

A middleware processes request data and calls `next()` method
if the execution chain should continue running the following middleware.

Middleware can be used globally before all listener executions.
It&#x27;s also possible to run a middleware only for a particular listener.

## SingleTeamAuthorization Objects

```python
class SingleTeamAuthorization(Authorization)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

## MultiTeamsAuthorization Objects

```python
class MultiTeamsAuthorization(Authorization)
```

#### authorize

#### user\_token\_resolution

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

## CustomMiddleware Objects

```python
class CustomMiddleware(Middleware)
```

#### app\_name

#### func

#### arg\_names

#### logger

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

#### name

```python
@property
def name() -> str
```

## IgnoringSelfEvents Objects

```python
class IgnoringSelfEvents(Middleware)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

#### events\_that\_should\_be\_kept

## Middleware Objects

```python
class Middleware(metaclass=ABCMeta)
```

A middleware can process request data before other middleware and listener functions.

#### process

```python
@abstractmethod
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

Processes a request data before other middleware and listeners.
A middleware calls `next()` function if the chain should continue.

```python
    @app.middleware
    def simple_middleware(req, resp, next):
        # do something here
        next()
```

This `process(req, resp, next)` method is supposed to be invoked only inside bolt-python.
If you want to avoid the name `next()` in your middleware functions, you can use `next_()` method instead.

```python
    @app.middleware
    def simple_middleware(req, resp, next_):
        # do something here
        next_()
```

**Arguments**:

- `req` - The incoming request
- `resp` - The response
- `next` - The function to tell the chain that it can continue
  

**Returns**:

  Processed response (optional)

#### name

```python
@property
def name() -> str
```

The name of this middleware

## RequestVerification Objects

```python
class RequestVerification(Middleware)
```

#### verifier

```python
@property
def verifier() -> SignatureVerifier
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

## SslCheck Objects

```python
class SslCheck(Middleware)
```

#### verification\_token

#### logger

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

## UrlVerification Objects

```python
class UrlVerification(Middleware)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

## AttachingFunctionToken Objects

```python
class AttachingFunctionToken(Middleware)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> BoltResponse
```

## AttachingConversationKwargs Objects

```python
class AttachingConversationKwargs(Middleware)
```

#### thread\_context\_store

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

#### builtin\_middleware\_classes

