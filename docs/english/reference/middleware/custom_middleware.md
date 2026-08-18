---
sidebar_label: custom_middleware
title: slack_bolt.middleware.custom_middleware
---

#### build\_required\_kwargs

```python
def build_required_kwargs(*,
                          logger: logging.Logger,
                          required_arg_names: MutableSequence[str],
                          request: BoltRequest,
                          response: Optional[BoltResponse],
                          next_func: Optional[Callable[[], None]] = None,
                          this_func: Optional[Callable] = None,
                          error: Optional[Exception] = None,
                          next_keys_required: bool = True) -> Dict[str, Any]
```

#### get\_bolt\_app\_logger

```python
def get_bolt_app_logger(app_name: str,
                        cls: object = None,
                        base_logger: Optional[Logger] = None) -> Logger
```

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body: `str`

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for &quot;http&quot; mode)

#### context: `BoltContext`

The context in this request.

#### lazy\_only: `bool`

#### lazy\_function\_name: `Optional[str]`

#### mode: `str`

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

#### status: `int`

HTTP status code

#### body: `str`

The response body (dict and str are supported)

#### headers: `Dict[str, Sequence[str]]`

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

#### get\_name\_for\_callable

```python
def get_name_for_callable(func: Callable) -> str
```

Returns the name for the given Callable function object.

**Arguments**:

- `func` - Either a `Callable` instance or a function, which as `__name__`
  

**Returns**:

  The name of the given Callable object

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
```

## CustomMiddleware Objects

```python
class CustomMiddleware(Middleware)
```

#### app\_name: `str`

#### func: `Callable[..., Any]`

#### arg\_names: `MutableSequence[str]`

#### logger: `Logger`

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             func: Callable,
             base_logger: Optional[Logger] = None)
```

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

