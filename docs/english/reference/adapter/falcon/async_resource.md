---
sidebar_label: async_resource
title: slack_bolt.adapter.falcon.async_resource
---

## AsyncSlackAppResource Objects

```python
class AsyncSlackAppResource()
```

For use with ASGI Falcon Apps.

from slack_bolt.async_app import AsyncApp
app = AsyncApp()

import falcon
app = falcon.asgi.App()
app.add_route("/slack/events", AsyncSlackAppResource(app))

#### \_\_init\_\_

```python
def __init__(app: AsyncApp)
```

#### on\_get

```python
async def on_get(req: Request, resp: Response)
```

#### on\_post

```python
async def on_post(req: Request, resp: Response)
```
