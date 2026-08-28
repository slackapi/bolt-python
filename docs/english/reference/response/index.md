---
sidebar_label: response
title: slack_bolt.response
---

This interface represents Bolt's synchronous response to Slack.

In Socket Mode, the response data can be transformed to a WebSocket message. In the HTTP endpoint mode,
the response data becomes an HTTP response data.

Refer to https://docs.slack.dev/apis/events-api/ for the two types of connections.

## `BoltResponse`

```python
BoltResponse(*, status, body='', headers=None)
```

The response from a Bolt app.

**Parameters:**

- **status** (int) – HTTP status code
- **body** (Union[str, dict]) – The response body (dict and str are supported)
- **headers** (Optional[Dict[str, Union[str, Sequence[str]]]]) – The response headers.

## Submodules

- [slack_bolt.response.response](/tools/bolt-python/reference/response/response)
