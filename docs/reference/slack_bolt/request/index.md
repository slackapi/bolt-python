---
sidebar_label: request
title: slack_bolt.request
---

Incoming request from Slack through either HTTP request or Socket Mode connection.

Refer to https://docs.slack.dev/apis/events-api/ for the two types of connections.
This interface encapsulates the difference between the two.

## BoltRequest Objects

```python
class BoltRequest()
```

#### raw\_body

#### query

#### headers

#### content\_type

#### body

#### context

#### lazy\_only

#### lazy\_function\_name

#### mode

either &quot;http&quot; or &quot;socket_mode&quot;

#### to\_copyable

```python
def to_copyable() -> "BoltRequest"
```

