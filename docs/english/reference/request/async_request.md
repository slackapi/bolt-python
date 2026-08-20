---
sidebar_label: async_request
title: slack_bolt.request.async_request
---

## AsyncBoltRequest Objects

```python
class AsyncBoltRequest()
```

#### raw\_body: `str`

#### body: `Dict[str, Any]`

The raw request body (only plain text is supported for "http" mode)

#### query: `Dict[str, Sequence[str]]`

The query string data in any data format.

#### headers: `Dict[str, Sequence[str]]`

The request headers.

#### content\_type: `Optional[str]`

#### context: `AsyncBoltContext`

The context in this request.

#### lazy\_only: `bool`

#### lazy\_function\_name: `Optional[str]`

#### mode: `str`

The mode used for this request. (either "http" or "socket_mode")

#### \_\_init\_\_

```python
def __init__(
    *,
    body: Union[str, dict],
    query: Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]] = None,
    headers: Optional[Dict[str, Union[str, Sequence[str]]]] = None,
    context: Optional[Dict[str, Any]] = None,
    mode: str = 'http')
```

Request to a Bolt app.

**Arguments**:

- `body` _Union[str, dict]_ - The raw request body (only plain text is supported for "http" mode)
- `query` _Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]]_ - The query string data in any data format.
- `headers` _Optional[Dict[str, Union[str, Sequence[str]]]]_ - The request headers.
- `context` _Optional[Dict[str, Any]]_ - The context in this request.
- `mode` _str_ - The mode used for this request. (either "http" or "socket_mode")

#### to\_copyable

```python
def to_copyable() -> AsyncBoltRequest
```
