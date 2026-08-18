---
sidebar_label: internals
title: slack_bolt.context.ack.internals
---

## BoltError Objects

```python
class BoltError(Exception)
```

General class in a Bolt app

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

#### convert\_to\_dict\_list

```python
def convert_to_dict_list(
        objects: Sequence[Union[Dict, JsonObject]]) -> Sequence[Dict]
```

#### convert\_to\_dict

```python
def convert_to_dict(obj: Union[Dict, JsonObject]) -> Dict
```

