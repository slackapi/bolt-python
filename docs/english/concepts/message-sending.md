# Sending messages

Within your listener function, `say()` is available whenever there is an associated conversation (for example, a conversation where the event or action which triggered the listener occurred). `say()` accepts a string to post simple messages and JSON payloads to send more complex messages. The message payload you pass in will be sent to the associated conversation.

In the case that you'd like to send a message outside of a listener or you want to do something more advanced (like handle specific errors), you can call `client.chat_postMessage` [using the client attached to your Bolt instance](/tools/bolt-python/concepts/web-api).

Refer to [the module document](https://docs.slack.dev/tools/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.

```python
# Listens for messages containing "knock knock" and responds with an italicized "who's there?"
@app.message("knock knock")
def ask_who(message, say):
    say("_Who's there?_")
```

## Sending a message with blocks

`say()` accepts more complex message payloads to make it easy to add functionality and structure to your messages.

To explore adding rich message layouts to your app, read through [the guide on our API site](/messaging/#structure) and look through templates of common app flows [in the Block Kit Builder](https://api.slack.com/tools/block-kit-builder?template=1).

```python
# Sends a section block with datepicker when someone reacts with a 📅 emoji
@app.event("reaction_added")
def show_datepicker(event, say):
    reaction = event["reaction"]
    if reaction == "calendar":
        blocks = [{
          "type": "section",
          "text": {"type": "mrkdwn", "text": "Pick a date for me to remind you"},
          "accessory": {
              "type": "datepicker",
              "action_id": "datepicker_remind",
              "initial_date": "2020-05-04",
              "placeholder": {"type": "plain_text", "text": "Select a date"}
          }
        }]
        say(
            blocks=blocks,
            text="Pick a date for me to remind you"
        )
```

## Streaming messages {#streaming-messages}

You can have your app's messages stream in to replicate conventional agent behavior. Bolt for Python provides a `say_stream` utility as a listener argument available for `app.event` and `app.message` listeners. 

The `say_stream` utility streamlines calling the Python Slack SDK's [`WebClient.chat_stream`](https://docs.slack.dev/tools/python-slack-sdk/reference/web/client.html#slack_sdk.web.client.WebClient.chat_stream) helper utility by sourcing parameter values from the relevant event payload.

| Parameter | Value |
|---|---| 
| `channel_id` | Sourced from the event payload.
| `thread_ts` | Sourced from the event payload. Falls back to the `ts` value if available.
| `recipient_team_id` | Sourced from the event `team_id` (`enterprise_id` if the app is installed on an org).
| `recipient_user_id` | Sourced from the `user_id` of the event.

If neither a `channel_id` or `thread_ts` can be sourced, then the utility will be `None`.

For information on calling the `chat_*Stream` API methods directly, see the [_Sending streaming messages_](/tools/python-slack-sdk/web#sending-streaming-messages) section of the Python Slack SDK docs.

### Example {#example}

```py
import os

from slack_bolt import App, SayStream
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("app_mention")
def handle_app_mention(client: WebClient, say_stream: SayStream):
  stream = say_stream()
  stream.append(markdown_text="Someone rang the bat signal!")
  stream.stop()

@app.message("")
def handle_message(client: WebClient, say_stream: SayStream):
  stream = say_stream()

  stream.append(markdown_text="Let me consult my *vast knowledge database*...)
  stream.stop()

if __name__ == "__main__":
  SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
```

#### Adding feedback buttons after a stream

You can pass a [feedback buttons](/reference/block-kit/block-elements/feedback-buttons-element) block element to `stream.stop` to provide feedback buttons to the user at the bottom of the message. Interaction with these buttons will send a block action event to your app to receive the feedback.

```py
stream.stop(blocks=feedback_block)
```

```py
def create_feedback_block() -> List[Block]:
    blocks: List[Block] = [
        ContextActionsBlock(
            elements=[
                FeedbackButtonsElement(
                    action_id="feedback",
                    positive_button=FeedbackButtonObject(
                        text="Good Response",
                        accessibility_label="Submit positive feedback on this response",
                        value="good-feedback",
                    ),
                    negative_button=FeedbackButtonObject(
                        text="Bad Response",
                        accessibility_label="Submit negative feedback on this response",
                        value="bad-feedback",
                    ),
                )
            ]
        )
    ]
    return blocks
```