# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "..")
# ------------------------------------------------

import logging
from typing import Callable
from logging import Logger
from slack_bolt import App, BoltResponse, Ack, Respond
from slack_sdk import WebClient
from slack_sdk.models.blocks import (
    PlainTextObject,
    InputBlock,
    PlainTextInputElement,
    ExternalDataSelectElement,
    ExternalDataMultiSelectElement,
    Option,
    OptionGroup,
    SectionBlock,
    MarkdownTextObject,
    ButtonElement,
)
from slack_sdk.models.views import View

logging.basicConfig(level=logging.DEBUG)

app = App()


@app.middleware  # or app.use(log_request)
def log_request(
    logger: Logger, body: dict, next: Callable[[], BoltResponse]
) -> BoltResponse:
    logger.debug(body)
    return next()


@app.command("/hello-bolt-python")
def handle_command(
    body: dict, ack: Ack, respond: Respond, client: WebClient, logger: Logger
) -> None:
    logger.info(body)
    ack(
        text="Accepted!",
        blocks=[
            SectionBlock(
                block_id="b",
                text=MarkdownTextObject(text=":white_check_mark: Accepted!"),
            )
        ],
    )

    respond(
        blocks=[
            SectionBlock(
                block_id="b",
                text=MarkdownTextObject(
                    text="You can add a button alongside text in your message. "
                ),
                accessory=ButtonElement(
                    action_id="a",
                    text=PlainTextObject(text="Button"),
                    value="click_me_123",
                ),
            ),
        ]
    )

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view=View(
            type="modal",
            callback_id="view-id",
            title=PlainTextObject(text="My App"),
            submit=PlainTextObject(text="Submit"),
            close=PlainTextObject(text="Cancel"),
            blocks=[
                InputBlock(
                    element=PlainTextInputElement(action_id="text"),
                    label=PlainTextObject(text="Label"),
                ),
                InputBlock(
                    block_id="es_b",
                    element=ExternalDataSelectElement(
                        action_id="es_a",
                        placeholder=PlainTextObject(text="Select an item"),
                        min_query_length=0,
                    ),
                    label=PlainTextObject(text="Search"),
                ),
                InputBlock(
                    block_id="mes_b",
                    element=ExternalDataMultiSelectElement(
                        action_id="mes_a",
                        placeholder=PlainTextObject(text="Select an item"),
                        min_query_length=0,
                    ),
                    label=PlainTextObject(text="Search (multi)"),
                ),
            ],
        ),
    )
    logger.info(res)


@app.options("es_a")
def show_options(ack: Ack) -> None:
    ack(options=[Option(text=PlainTextObject(text="Maru"), value="maru")])


@app.options("mes_a")
def show_multi_options(ack: Ack) -> None:
    ack(
        option_groups=[
            OptionGroup(
                label=PlainTextObject(text="Group 1"),
                options=[
                    Option(text=PlainTextObject(text="Option 1"), value="1-1"),
                    Option(text=PlainTextObject(text="Option 2"), value="1-2"),
                ],
            ),
            OptionGroup(
                label=PlainTextObject(text="Group 2"),
                options=[Option(text=PlainTextObject(text="Option 1"), value="2-1"),],
            ),
        ]
    )


@app.view("view-id")
def view_submission(ack: Ack, body: dict, logger: Logger) -> None:
    ack()
    logger.info(body["view"]["state"]["values"])


@app.action("a")
def button_click(ack: Ack, body: dict, respond: Respond) -> None:
    ack()

    user_id: str = body["user"]["id"]
    # in_channel / dict
    respond(
        response_type="in_channel",
        replace_original=False,
        text=f"<@{user_id}> clicked a button! (in_channel)",
    )
    # ephemeral / kwargs
    respond(
        replace_original=False, text=":white_check_mark: Done!",
    )


if __name__ == "__main__":
    app.start(3000)

# pip install slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python modals_app_typed.py
