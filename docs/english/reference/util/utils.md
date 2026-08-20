---
sidebar_label: utils
title: slack_bolt.util.utils
---

#### create\_web\_client

```python
def create_web_client(
    token: Optional[str] = None,
    logger: Optional[Logger] = None) -> WebClient
```

#### convert\_to\_dict\_list

```python
def convert_to_dict_list(objects: Sequence[Union[Dict, JsonObject]]) -> Sequence[Dict]
```

#### convert\_to\_dict

```python
def convert_to_dict(obj: Union[Dict, JsonObject]) -> Dict
```

#### create\_copy

```python
def create_copy(original: Any) -> Any
```

#### get\_boot\_message

```python
def get_boot_message(development_server: bool = False) -> str
```

#### get\_name\_for\_callable

```python
def get_name_for_callable(func: Callable) -> str
```

Returns the name for the given Callable function object.

**Arguments**:

- `func` _Callable_ - Either a `Callable` instance or a function, which as `__name__`

**Returns**:

- `str` - The name of the given Callable object

#### get\_arg\_names\_of\_callable

```python
def get_arg_names_of_callable(func: Callable) -> List[str]
```

#### is\_callable\_coroutine

```python
def is_callable_coroutine(func: Optional[Any]) -> bool
```

#### is\_used\_without\_argument

```python
def is_used_without_argument(args) -> bool
```

Tests if a decorator invocation is without () or (args).

**Arguments**:

- `args` - arguments

**Returns**:

- `bool` - True if it's an invocation without args
