---
title: Using Socket Mode
lang: en
slug: socket-mode
order: 16
---

<div class="section-content">
With the introduction of [Socket Mode](ADD api.slack.com link when ready), Bolt for Python introduced support in version `1.2.0`. With Socket Mode, instead of creating a server with endpoints that Slack sends payloads too, the app will instead connect to Slack via a WebSocket connection and receive data from Slack over the socket connection. Make sure to enable Socket Mode in your app configuration settings. 

To use the Socket Mode, add `SLACK_APP_TOKEN` as an environment variable. You can get your App Token in your app configuration settings under the **Basic Information** section. 
</div>

```python
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])

if __name__ == "__main__":
    # export SLACK_APP_TOKEN=xapp-***
    # export SLACK_BOT_TOKEN=xoxb-***
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```
