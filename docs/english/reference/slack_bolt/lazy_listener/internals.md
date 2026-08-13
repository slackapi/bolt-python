---
sidebar_label: internals
title: slack_bolt.lazy_listener.internals
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

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
```

#### build\_runnable\_function

```python
def build_runnable_function(func: Callable[..., None], logger: Logger,
                            request: BoltRequest) -> Callable[[], None]
```

