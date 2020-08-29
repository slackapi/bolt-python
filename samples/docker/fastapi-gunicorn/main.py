import logging

from slack_bolt.async_app import AsyncApp

logging.basicConfig(level=logging.DEBUG)
app = AsyncApp()


@app.command("/hello-bolt-python")
async def hello(payload, ack, logger):
    user_id = payload["user_id"]
    await ack(f"Hi! <@{user_id}>")


from fastapi import FastAPI, Request

api = FastAPI()

from slack_bolt.adapter.fastapi import AsyncSlackRequestHandler

app_handler = AsyncSlackRequestHandler(app)


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)
