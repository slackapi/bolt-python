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

You can have your app's messages stream in to replicate conventional AI chatbot behavior. This is done through three Web API methods:

* [`chat_startStream`](/reference/methods/chat.startstream)
* [`chat_appendStream`](/reference/methods/chat.appendstream)
* [`chat_stopStream`](/reference/methods/chat.stopstream)

The Python Slack SDK provides a [`chat_stream()`](https://docss.slack.dev/tools/python-slack-sdk/reference/web/client.html#slack_sdk.web.client.WebClient.chat_stream) helper utility to streamline calling these methods. Here's an excerpt from our [Assistant template app](https://github.com/slack-samples/bolt-python-assistant-template/blob/main/listeners/assistant/assistant.py)

```python
streamer = client.chat_stream(
    channel=channel_id,
    recipient_team_id=team_id,
    recipient_user_id=user_id,
    thread_ts=thread_ts,
)

for event in returned_message:
    if event.type == "response.output_text.delta":
        streamer.append(markdown_text=f"{event.delta}")
    else:
        continue

feedback_block = create_feedback_block()
streamer.stop(blocks=feedback_block)
```

In that example, a [feedback buttons](/reference/block-kit/block-elements/feedback-buttons-element) block element is passed to `streamer.stop` — this provides feedback buttons to the user at the bottom of the message.

```python
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

For information on calling the `chat_*Stream` API methods without the helper utility, see the [_Sending streaming messages_](/tools/python-slack-sdk/web#sending-streaming-messages) section of the Python Slack SDK docs.