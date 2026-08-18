---
sidebar_label: step_middleware
title: slack_bolt.workflows.step.step_middleware
---

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

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body

#### query

The query string data in any data format.

#### headers

The request headers.

#### content\_type

#### body

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### context

The context in this request.

#### lazy\_only

#### lazy\_function\_name

#### mode

The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

#### \_\_init\_\_

```python
def __init__(*,
             body: Union[str, dict],
             query: Optional[Union[str, Dict[str, str],
                                   Dict[str, Sequence[str]]]] = None,
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
             context: Optional[Dict[str, Any]] = None,
             mode: str = "http")
```

Request to a Bolt app.

**Arguments**:

- `body` - The raw request body (only plain text is supported for &quot;http&quot; mode)
- `query` - The query string data in any data format.
- `headers` - The request headers.
- `context` - The context in this request.
- `mode` - The mode used for this request. (either &quot;http&quot; or &quot;socket_mode&quot;)

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

HTTP status code

#### body

The response body (dict and str are supported)

#### headers

The response headers.

#### \_\_init\_\_

```python
def __init__(*,
             status: int,
             body: Union[str, dict] = "",
             headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None)
```

The response from a Bolt app.

**Arguments**:

- `status` - HTTP status code
- `body` - The response body (dict and str are supported)
- `headers` - The response headers.

#### first\_headers

```python
def first_headers() -> Dict[str, str]
```

#### first\_headers\_without\_set\_cookie

```python
def first_headers_without_set_cookie() -> Dict[str, str]
```

#### cookies

```python
def cookies() -> Sequence[SimpleCookie]
```

#### get\_name\_for\_callable

```python
def get_name_for_callable(func: Callable) -> str
```

Returns the name for the given Callable function object.

**Arguments**:

- `func` - Either a `Callable` instance or a function, which as `__name__`
  

**Returns**:

  The name of the given Callable object

## WorkflowStep Objects

```python
class WorkflowStep()
```

#### callback\_id

The Callback ID of the step from app

#### edit

`edit` listener, which displays a modal in Workflow Builder

#### save

`save` listener, which accepts workflow creator&#x27;s data submission in Workflow Builder

#### execute

`execute` listener, which processes step from app execution

#### \_\_init\_\_

```python
def __init__(*,
             callback_id: Union[str, Pattern],
             edit: Union[Callable[..., Optional[BoltResponse]], Listener,
                         Sequence[Callable]],
             save: Union[Callable[..., Optional[BoltResponse]], Listener,
                         Sequence[Callable]],
             execute: Union[Callable[..., Optional[BoltResponse]], Listener,
                            Sequence[Callable]],
             app_name: Optional[str] = None,
             base_logger: Optional[Logger] = None)
```

Deprecated:
Steps from apps for legacy workflows are now deprecated.
Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

**Arguments**:

- `callback_id` - The callback_id for this step from app
- `edit` - Either a single function or a list of functions for opening a modal in the builder UI
  When it&#x27;s a list, the first one is responsible for ack() while the rest are lazy listeners.
- `save` - Either a single function or a list of functions for handling modal interactions in the builder UI
  When it&#x27;s a list, the first one is responsible for ack() while the rest are lazy listeners.
- `execute` - Either a single function or a list of functions for handling step from app executions
  When it&#x27;s a list, the first one is responsible for ack() while the rest are lazy listeners.
- `app_name` - The app name that can be mainly used for logging
- `base_logger` - The logger instance that can be used as a template when creating this step&#x27;s logger

#### builder

```python
@classmethod
def builder(cls,
            callback_id: Union[str, Pattern],
            base_logger: Optional[Logger] = None) -> WorkflowStepBuilder
```

Deprecated:
    Steps from apps for legacy workflows are now deprecated.
    Use new custom steps: https://docs.slack.dev/workflows/workflow-steps/

#### build\_listener

```python
@classmethod
def build_listener(cls,
                   callback_id: Union[str, Pattern],
                   app_name: str,
                   listener_or_functions: Union[Listener, Callable,
                                                List[Callable]],
                   name: str,
                   matchers: Optional[List[ListenerMatcher]] = None,
                   middleware: Optional[List[Middleware]] = None,
                   base_logger: Optional[Logger] = None) -> Listener
```

## WorkflowStepMiddleware Objects

```python
class WorkflowStepMiddleware(Middleware)
```

Base middleware for step from app specific ones

#### \_\_init\_\_

```python
def __init__(step: WorkflowStep)
```

#### process

```python
def process(*, req: BoltRequest, resp: BoltResponse,
            next: Callable[[], BoltResponse]) -> Optional[BoltResponse]
```

