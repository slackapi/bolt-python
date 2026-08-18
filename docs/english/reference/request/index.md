---
sidebar_label: request
title: slack_bolt.request
---


Incoming request from Slack through either HTTP request or Socket Mode connection.

Refer to https://docs.slack.dev/apis/events-api/ for the two types of connections.
This interface encapsulates the difference between the two.

## Submodules

- [slack_bolt.request.async_internals](/tools/bolt-python/reference/request/async_internals)
- [slack_bolt.request.async_request](/tools/bolt-python/reference/request/async_request)
- [slack_bolt.request.internals](/tools/bolt-python/reference/request/internals)
- [slack_bolt.request.payload_utils](/tools/bolt-python/reference/request/payload_utils)
- [slack_bolt.request.request](/tools/bolt-python/reference/request/request)

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

