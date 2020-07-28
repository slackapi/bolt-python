from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler

app = App()


@app.event("app_mention")
def event_test(ack, payload, say, logger):
    logger.info(payload)
    say("What's up?")


handler = SlackRequestHandler(app=app)


@csrf_exempt
def handle(request: HttpRequest):
    return handler.handle(request)
