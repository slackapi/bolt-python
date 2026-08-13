---
sidebar_label: falcon
title: slack_bolt.adapter.falcon
---

## SlackAppResource Objects

```python
class SlackAppResource()
```

```python
from slack_bolt import App
app = App()

import falcon
api = application = falcon.API()
api.add_route("/slack/events", SlackAppResource(app))
```

#### on\_get

```python
def on_get(req: Request, resp: Response)
```

#### on\_post

```python
def on_post(req: Request, resp: Response)
```

