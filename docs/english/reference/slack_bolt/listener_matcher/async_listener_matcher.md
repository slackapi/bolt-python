---
sidebar_label: async_listener_matcher
title: slack_bolt.listener_matcher.async_listener_matcher
---

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body

#### body

#### query

#### headers

#### content\_type

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

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
def to_copyable() -> "AsyncBoltRequest"
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

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

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
```

## AsyncListenerMatcher Objects

```python
class AsyncListenerMatcher(metaclass=ABCMeta)
```

#### async\_matches

```python
@abstractmethod
async def async_matches(req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

Matches against the request and returns True if matched.

**Arguments**:

- `req` - The request
- `resp` - The response
  

**Returns**:

  True if matched

#### build\_async\_required\_kwargs

```python
def build_async_required_kwargs(
        *,
        logger: logging.Logger,
        required_arg_names: MutableSequence[str],
        request: AsyncBoltRequest,
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

## AsyncCustomListenerMatcher Objects

```python
class AsyncCustomListenerMatcher(AsyncListenerMatcher)
```

#### app\_name

#### func

#### arg\_names

#### logger

#### \_\_init\_\_

```python
def __init__(*,
             app_name: str,
             func: Callable[..., Awaitable[bool]],
             base_logger: Optional[Logger] = None)
```

#### async\_matches

```python
async def async_matches(req: AsyncBoltRequest, resp: BoltResponse) -> bool
```

#### builtin\_async\_listener\_matcher\_classes

