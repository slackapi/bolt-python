---
sidebar_label: async_resource
title: slack_bolt.adapter.falcon.async_resource
---

## `AsyncSlackAppResource`

```python
AsyncSlackAppResource(app)
```

For use with ASGI Falcon Apps.

```python
from slack_bolt.async_app import AsyncApp

app = AsyncApp()

import falcon

app = falcon.asgi.App()
app.add_route("/slack/events", AsyncSlackAppResource(app))
```
