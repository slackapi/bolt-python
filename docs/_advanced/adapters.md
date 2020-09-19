---
title: Using in Web frameworks
lang: en
slug: adapters
order: 0
---

<div class="section-content">
`App#start()` starts a Web server process using the [`http.server` standard library](https://docs.python.org/3/library/http.server.html). As mentioned in its document, it is not recommended to use the module for production.

Once you're done with local development, it's about time to choose the right Web framework and production-ready server.

Let's try using [Flask](https://flask.palletsprojects.com/) framework along with the [Gunicorn](https://gunicorn.org/) WSGI HTTP server here.

```bash
pip install slack_bolt flask gunicorn
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
# Save the source code as main.py
gunicorn --bind :3000 --workers 1 --threads 2 --timeout 0 main:flask_app
```

We currently support the following frameworks. As long as a Web framework works, you can run Bolt app in any web servers.

* [Django](https://www.djangoproject.com/)
* [Flask](https://flask.palletsprojects.com/)
* [Starlette](https://www.starlette.io/) & [FastAPI](https://fastapi.tiangolo.com/)
* [Sanic](https://sanicframework.org/)
* [Tornado](https://www.tornadoweb.org/)
* [Falcon](https://falcon.readthedocs.io/)
* [Bottle](https://bottlepy.org/)
* [CherryPy](https://cherrypy.org/)
* [Pyramid](https://trypyramid.com/)

Check [samples](https://github.com/slackapi/bolt-python/tree/main/samples) in the GitHub repository to learn how to configure your app with frameworks.

</div>

```python
from slack_bolt import App
app = App()

# There is nothing specific to Flask here!
# App is completely framework/runtime agnostic
@app.command("/hello-bolt")
def hello(body, ack):
    ack(f"Hi <@{body['user_id']}>!")

# Initialize Flask app
from flask import Flask, request
flask_app = Flask(__name__)

# SlackRequestHandler translates WSGI requests to Bolt's interface
# and builds WSGI response from Bolt's response.
from slack_bolt.adapter.flask import SlackRequestHandler
handler = SlackRequestHandler(app)

# Register routes to Flask app
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # handler runs App's dispatch method
    return handler.handle(request)
```
