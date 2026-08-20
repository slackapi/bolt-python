---
sidebar_label: response
title: slack_bolt.response.response
slug: response
---

## BoltResponse Objects

```python
class BoltResponse()
```

#### status: `int`

#### body: `str`

#### headers: `Dict[str, Sequence[str]]`

#### \_\_init\_\_

```python
def __init__(
    *,
    status: int,
    body: Union[str, dict] = '',
    headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None)
```

The response from a Bolt app.

**Arguments**:

- `status` _int_ - HTTP status code
- `body` _Union[str, dict]_ - The response body (dict and str are supported)
- `headers` _Optional[Dict[str, Union[str, Sequence[str]]]]_ - The response headers.

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
