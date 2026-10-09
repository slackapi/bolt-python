---
sidebar_label: response
title: slack_bolt.response.response
slug: response
---

## `BoltResponse`

```python
BoltResponse(*, status, body='', headers=None)
```

The response from a Bolt app.

**Parameters:**

- **status** (int) – HTTP status code
- **body** (Union[str, dict]) – The response body (dict and str are supported)
- **headers** (Optional[Dict[str, Union[str, Sequence[str]]]]) – The response headers.
