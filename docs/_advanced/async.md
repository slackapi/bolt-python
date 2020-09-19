---
title: Async Bolt
lang: en
slug: advanced-async
order: 1
---

<div class="section-content">
In the Basic concepts section, all the code snippets are not in the asynchronous programming style. You may be wondering if Bolt for Python is not available for asynchronous frameworks and their runtime such as the standard `asyncio` library.

No worries! You can use Bolt with [Starlette](https://www.starlette.io/), [FastAPI](https://fastapi.tiangolo.com/), [Sanic](https://sanicframework.org/), [AIOHTTP](https://docs.aiohttp.org/), and whatever you want to use.

`AsyncApp` internally relies on AIOHTTP for making HTTP requests to Slack API servers. So, to use the async version of Bolt, add `aiohttp` to `requirements.txt` or run `pip install aiohttp`.

You can find sample projects in [samples](https://github.com/slackapi/bolt-python/tree/main/samples) directory in the GitHub repository.

</div>

```python
# required: pip install aiohttp
from slack_bolt.async_app import AsyncApp
app = AsyncApp()

@app.event("app_mention")
async def handle_mentions(event, client, say):  # async function
    api_response = await client.reactions_add(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )
    await say("What's up?")

if __name__ == "__main__":
    app.start(3000)
```

<details class="secondary-wrapper">
<summary class="section-head" markdown="0">
<h4 class="section-head">Using other async frameworks</h4>
</summary>

<div class="secondary-content" markdown="0">

`AsyncApp#start()` internally uses [AIOHTTP](https://docs.aiohttp.org/)'s web server feature. However, this doesn't mean you have to use AIOHTTP. `AsyncApp` can handle incoming requests from Slack using any other frameworks.

The code snippet in this section is an example using [Sanic](https://sanicframework.org/). You can start your Slack app server-side built with Sanic only by running the following commands.

```bash
pip install slack_bolt sanic uvicorn
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
# save the source as async_app.py
uvicorn async_app:api --reload --port 3000 --log-level debug
```

If you would like to use other frameworks, check the list of the built-in adapters [here](https://github.com/slackapi/bolt-python/tree/main/slack_bolt/adapter). If your favorite framework is available there, you can use Bolt with it in a similar way.

</div>

```python
from slack_bolt.async_app import AsyncApp
app = AsyncApp()

# There is nothing specific to Sanic here!
# AsyncApp is completely framework/runtime agnostic
@app.event("app_mention")
async def handle_app_mentions(say):
    await say("What's up?")

import os
from sanic import Sanic
from sanic.request import Request
from slack_bolt.adapter.sanic import AsyncSlackRequestHandler

# Create an adapter for Sanic with the App instance
app_handler = AsyncSlackRequestHandler(app)
# Create a Sanic app
api = Sanic(name="awesome-slack-app")

@api.post("/slack/events")
async def endpoint(req: Request):
    # app_handler internally runs the App's dispatch method
    return await app_handler.handle(req)

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
```

</details>
