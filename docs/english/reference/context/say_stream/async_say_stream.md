---
sidebar_label: async_say_stream
title: slack_bolt.context.say_stream.async_say_stream
---

## AsyncSayStream Objects

```python
class AsyncSayStream()
```

#### client: `AsyncWebClient`

#### channel: `Optional[str]`

#### recipient\_team\_id: `Optional[str]`

#### recipient\_user\_id: `Optional[str]`

#### thread\_ts: `Optional[str]`

#### \_\_init\_\_

```python
def __init__(*,
             client: AsyncWebClient,
             channel: Optional[str] = None,
             recipient_team_id: Optional[str] = None,
             recipient_user_id: Optional[str] = None,
             thread_ts: Optional[str] = None)
```

