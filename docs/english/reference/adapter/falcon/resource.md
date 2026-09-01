---
sidebar_label: resource
title: slack_bolt.adapter.falcon.resource
---

## `SlackAppResource`

```python
SlackAppResource(app)
```

For use with WSGI Falcon Apps.

```python
from slack_bolt import App

app = App()

import falcon

api = application = falcon.API()
api.add_route("/slack/events", SlackAppResource(app))
```
