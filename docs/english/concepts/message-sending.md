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

## Streaming messages 

You can have your app's messages stream in for those AI chatbot vibes. This is done through three methods:

* `chat_startStream`
* `chat_appendStream`
* `chat_stopStream`

### Starting the message stream

First you need to begin the message stream.

```python
# Example: Stream a response to any message
@app.message()
def handle_message(message, client):
    channel_id = payload["channel"]
    thread_ts = payload["thread_ts"]
    
    # Start a new message stream
    stream_response = client.chat_startStream(
        channel=channel_id,
        thread_ts=thread_ts,
    )
    stream_ts = stream_response["ts"]
```

### Appending content to the message stream

With the stream started, you can then append text to it in chunks to convey a streaming effect.

The structure of the text coming in will depend on your source. The following code snippet uses OpenAI's response structure as an example. 

```python
# continued from above
    for event in returned_message:
        if event.type == "response.output_text.delta":
            client.chat_appendStream(
                channel=channel_id, 
                ts=stream_ts, 
                markdown_text=f"{event.delta}"
            )
        else:
            continue
```

### Finishing the message stream

Your app can then end the stream with the `chat_stopStream` method. 

```python
# continued from above
    client.chat_stopStream(
        channel=channel_id, 
        ts=stream_ts
    )
```

The method also provides you an opportunity to request user feedback on your app's responses using the [feedback buttons](/reference/block-kit/block-elements/feedback-buttons-element) block element within the [context actions](/reference/block-kit/blocks/context-actions-block) block. The user will be presented with thumbs up and thumbs down buttons

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

@app.message()
def handle_message(message, client):
    # ... previous streaming code ...
    
    # Stop the stream and add interactive elements
    feedback_block = create_feedback_block()
    client.chat_stopStream(
        channel=channel_id, 
        ts=stream_ts, 
        blocks=feedback_block
    )
```