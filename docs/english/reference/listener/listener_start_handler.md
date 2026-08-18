---
sidebar_label: listener_start_handler
title: slack_bolt.listener.listener_start_handler
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

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
```

## ListenerStartHandler Objects

```python
class ListenerStartHandler(metaclass=ABCMeta)
```

#### handle

```python
@abstractmethod
def handle(request: BoltRequest, response: Optional[BoltResponse]) -> None
```

Do something extra before the listener execution.

This handler is useful if a developer needs to maintain/clean up
thread-local resources such as Django ORM database connections
before a listener execution starts.

**Arguments**:

- `request` - The request.
- `response` - The response.

## CustomListenerStartHandler Objects

```python
class CustomListenerStartHandler(ListenerStartHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger, func: Callable[..., None])
```

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse])
```

## DefaultListenerStartHandler Objects

```python
class DefaultListenerStartHandler(ListenerStartHandler)
```

#### \_\_init\_\_

```python
def __init__(logger: Logger)
```

#### handle

```python
def handle(request: BoltRequest, response: Optional[BoltResponse])
```

