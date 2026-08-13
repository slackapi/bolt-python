---
sidebar_label: middleware_error_handler
title: slack_bolt.middleware.middleware_error_handler
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

#### headers

#### content\_type

#### body

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
```

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

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

## MiddlewareErrorHandler Objects

```python
class MiddlewareErrorHandler(metaclass=ABCMeta)
```

#### handle

```python
@abstractmethod
def handle(error: Exception, request: BoltRequest,
           response: Optional[BoltResponse]) -> None
```

Handles an unhandled exception.

**Arguments**:

- `error` - The raised exception.
- `request` - The request.
- `response` - The response.

## CustomMiddlewareErrorHandler Objects

```python
class CustomMiddlewareErrorHandler(MiddlewareErrorHandler)
```

#### handle

```python
def handle(error: Exception, request: BoltRequest,
           response: Optional[BoltResponse])
```

## DefaultMiddlewareErrorHandler Objects

```python
class DefaultMiddlewareErrorHandler(MiddlewareErrorHandler)
```

#### handle

```python
def handle(error: Exception, request: BoltRequest,
           response: Optional[BoltResponse])
```

