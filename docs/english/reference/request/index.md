---
sidebar_label: request
title: slack_bolt.request
---

Incoming request from Slack through either HTTP request or Socket Mode connection.

Refer to https://docs.slack.dev/apis/events-api/ for the two types of connections.
This interface encapsulates the difference between the two.

## `BoltRequest`

```python
BoltRequest(*, body, query=None, headers=None, context=None, mode='http')
```

Request to a Bolt app.

**Parameters:**

- **body** (Union[str, dict]) – The raw request body (only plain text is supported for "http" mode)
- **query** (Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]]) – The query string data in any data format.
- **headers** (Optional[Dict[str, Union[str, Sequence[str]]]]) – The request headers.
- **context** (Optional[Dict[str, Any]]) – The context in this request.
- **mode** (str) – The mode used for this request. (either "http" or "socket_mode")

## Submodules

- [slack_bolt.request.async_internals](/tools/bolt-python/reference/request/async_internals)
- [slack_bolt.request.async_request](/tools/bolt-python/reference/request/async_request)
- [slack_bolt.request.internals](/tools/bolt-python/reference/request/internals)
- [slack_bolt.request.payload_utils](/tools/bolt-python/reference/request/payload_utils)
- [slack_bolt.request.request](/tools/bolt-python/reference/request/request)
