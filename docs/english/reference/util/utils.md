---
sidebar_label: utils
title: slack_bolt.util.utils
---

## `get_name_for_callable`

```python
get_name_for_callable(func)
```

Returns the name for the given Callable function object.

**Parameters:**

- **func** (Callable) – Either a `Callable` instance or a function, which as `__name__`

**Returns:**

- str – The name of the given Callable object

## `is_used_without_argument`

```python
is_used_without_argument(args)
```

Tests if a decorator invocation is without () or (args).

**Parameters:**

- **args** – arguments

**Returns:**

- bool – True if it's an invocation without args
