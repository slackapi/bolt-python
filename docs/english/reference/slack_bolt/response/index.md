---
sidebar_label: response
title: slack_bolt.response
---

This interface represents Bolt&#x27;s synchronous response to Slack.

In Socket Mode, the response data can be transformed to a WebSocket message. In the HTTP endpoint mode,
the response data becomes an HTTP response data.

Refer to https://docs.slack.dev/apis/events-api/ for the two types of connections.

## BoltResponse Objects

```python
class BoltResponse()
```

#### status

#### body

#### headers

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

