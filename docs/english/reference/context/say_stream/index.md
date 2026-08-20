---
sidebar_label: say_stream
title: slack_bolt.context.say_stream
---

## Submodules

- [slack_bolt.context.say_stream.async_say_stream](/tools/bolt-python/reference/context/say_stream/async_say_stream)
- [slack_bolt.context.say_stream.say_stream](/tools/bolt-python/reference/context/say_stream/say_stream)

## SayStream Objects

```python
class SayStream()
```

#### client: `WebClient`

#### channel: `Optional[str]`

#### recipient\_team\_id: `Optional[str]`

#### recipient\_user\_id: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(
    *,
    client: WebClient,
    channel: Optional[str] = None,
    recipient_team_id: Optional[str] = None,
    recipient_user_id: Optional[str] = None,
    thread_ts: Optional[str] = None)
```
