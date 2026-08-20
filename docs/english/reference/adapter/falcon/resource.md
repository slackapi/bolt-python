---
sidebar_label: resource
title: slack_bolt.adapter.falcon.resource
---

## SlackAppResource Objects

```python
class SlackAppResource()
```

from slack_bolt import App
app = App()

import falcon
api = application = falcon.API()
api.add_route("/slack/events", SlackAppResource(app))

#### \_\_init\_\_

```python
def __init__(app: App)
```

#### on\_get

```python
def on_get(req: Request, resp: Response)
```

#### on\_post

```python
def on_post(req: Request, resp: Response)
```
