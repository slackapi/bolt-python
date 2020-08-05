# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "..")
# ------------------------------------------------

import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App

app = App(process_before_response=True)


@app.middleware  # or app.use(log_request)
def log_request(logger, payload, next):
    logger.debug(payload)
    return next()


@app.command("/hello-bolt-python")
# or app.command(re.compile(r"/hello-.+"))(test_command)
def test_command(payload, respond, client, ack, logger):
    logger.info(payload)
    ack("Thanks!")

    respond(
        blocks=[
            {
                "type": "section",
                "block_id": "b",
                "text": {
                    "type": "mrkdwn",
                    "text": "You can add a button alongside text in your message. ",
                },
                "accessory": {
                    "type": "button",
                    "action_id": "a",
                    "text": {"type": "plain_text", "text": "Button"},
                    "value": "click_me_123",
                },
            }
        ]
    )

    res = client.views_open(
        trigger_id=payload["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "view-id",
            "title": {"type": "plain_text", "text": "My App",},
            "submit": {"type": "plain_text", "text": "Submit",},
            "close": {"type": "plain_text", "text": "Cancel",},
            "blocks": [
                {
                    "type": "input",
                    "element": {"type": "plain_text_input"},
                    "label": {"type": "plain_text", "text": "Label",},
                },
                {
                    "type": "input",
                    "block_id": "es_b",
                    "element": {
                        "type": "external_select",
                        "action_id": "es_a",
                        "placeholder": {"type": "plain_text", "text": "Select an item"},
                    },
                    "label": {"type": "plain_text", "text": "Search"},
                },
                {
                    "type": "input",
                    "block_id": "mes_b",
                    "element": {
                        "type": "multi_external_select",
                        "action_id": "mes_a",
                        "placeholder": {"type": "plain_text", "text": "Select an item"},
                    },
                    "label": {"type": "plain_text", "text": "Search (multi)"},
                },
            ],
        },
    )
    logger.info(res)


@app.options("es_a")
def show_options(ack):
    ack(
        {"options": [{"text": {"type": "plain_text", "text": "Maru"}, "value": "maru"}]}
    )


@app.options("mes_a")
def show_multi_options(ack):
    ack(
        {
            "option_groups": [
                {
                    "label": {"type": "plain_text", "text": "Group 1"},
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "Option 1"},
                            "value": "1-1",
                        },
                        {
                            "text": {"type": "plain_text", "text": "Option 2"},
                            "value": "1-2",
                        },
                    ],
                },
                {
                    "label": {"type": "plain_text", "text": "Group 2"},
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "Option 1"},
                            "value": "2-1",
                        },
                    ],
                },
            ]
        }
    )


@app.view("view-id")
def view_submission(ack, payload, logger):
    logger.info(payload)
    return ack()


@app.action("a")
def button_click(logger, payload, ack, respond):
    logger.info(payload)
    respond("respond!")
    # say(text="say!")
    ack()


if __name__ == "__main__":
    app.start(3000)

# pip install -i https://test.pypi.org/simple/ slack_bolt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# python modals_app.py
