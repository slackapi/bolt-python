---
sidebar_label: async_request
title: slack_bolt.request.async_request
---

## `AsyncBoltRequest`

```python
AsyncBoltRequest(*, body, query=None, headers=None, context=None, mode='http')
```

Request to a Bolt app.

**Parameters:**

- **body** (Union[str, dict]) – The raw request body (only plain text is supported for "http" mode)
- **query** (Optional[Union[str, Dict[str, str], Dict[str, Sequence[str]]]]) – The query string data in any data format.
- **headers** (Optional[Dict[str, Union[str, Sequence[str]]]]) – The request headers.
- **context** (Optional[Dict[str, Any]]) – The context in this request.
- **mode** (str) – The mode used for this request. (either "http" or "socket_mode")
