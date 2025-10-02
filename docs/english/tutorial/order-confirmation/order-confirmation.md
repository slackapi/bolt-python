---
title: Create a Salesforce order confirmation app
---

<Columns> 
  <Column>
    Learn how to use the Bolt for Python template and create a simple order confirmation app that links to systems of record—like Salesforce—in this tutorial.
  </Column>
  <Column> 
    ![Image of delivery tracker app](/img/bolt-python/delivery-tracker-main.png)
  </Column>
</Columns>

The scenario: you work for a large e-commerce company that employs many delivery workers. Those delivery workers don’t have access to a laptop when they’re on the go, but they do have access to Slack on their mobile devices. This tutorial teaches you how to create a simple Slack app that is geared towards these workers. Delivery drivers will enter order numbers on their mobile, along with some additional information about the order, and have that information sent to a channel in Slack and to a system of record. In this tutorial, Salesforce is our system of record.

You’ll also learn how to use the Bolt for Python starter app template and modify it to fit your needs. Note that this app is meant to be used for educational purposes and has not been tested rigorously enough to be used in production.

## Getting started

### Installing the Slack CLI

If you don't already have it, install the Slack CLI from your terminal. Navigate to [the installation guide](/slack-cli/guides/installing-the-slack-cli-for-mac-and-linux/) and follow the steps.

### Cloning the starter app

Once installed, use the command `slack create` in your terminal and find the `bolt-python-starter-template`. Alternatively, you can clone the [Bolt for Python template](https://github.com/slack-samples/bolt-python-starter-template) using git.

Optionally, you can remove the portions from the template that are not used within this tutorial to make things a bit cleaner for yourself. To do this, open your project and delete the commands, events, and shortcuts folders from the `/listeners` folder. You can also do the same to the corresponding folders within the `/listeners/tests` folder as well. Finally, remove the imports of these files from the `/listeners/__init__.py` file.

## Creating your app

We’ll use the contents of the `manifest.json` file below, which can also be found [here](https://github.com/wongjas/delivery-confirmation-app/blob/main/manifest.json). This file describes the metadata associated with your app, like its name and permissions that it requests.

Copy the contents of the file and [create a new app](https://api.slack.com/apps/new). Next, choose **From a manifest** and follow the prompts, pasting the manifest file contents you copied.

```json
{
  "_metadata": {
      "major_version": 1,
      "minor_version": 1
  },
  "display_information": {
      "name": "Name your app here!" 
  },
  "features": {
      "bot_user": {
          "display_name": "Name your app here!",
          "always_online": false
      }
  },
  "oauth_config": {
      "scopes": {
          "bot": [
              "channels:history",
              "chat:write"
          ]
      }
  },
  "settings": {
      "event_subscriptions": {
          "bot_events": [
              "message.channels"
          ]
      },
      "interactivity": {
          "is_enabled": true
      },
      "org_deploy_enabled": false,
      "socket_mode_enabled": true,
      "token_rotation_enabled": false
  }
}
```

Customize your app with a name of your own instead of the default in the `display_name` and `name` fields.

### Tokens

Once your app has been created, scroll down to **App-Level Tokens** on the **Basic Information** page and create a token that requests the [`connections:write`](/reference/scopes/connections.write) scope. This token will allow you to use [Socket Mode](/apis/events-api/using-socket-mode), which is a secure way to develop on Slack through the use of WebSockets. Save the value of your app token and store it in a safe place (we’ll use it in the next step).

### Install app

Install your app by navigating to **Install App** in the left sidebar. When you press **Allow**, this means you’re agreeing to install your app with the permissions that it’s requesting. Copy the bot token that you receive as well and store this in a safe place as well for subsequent steps.

## Starting your app's server

Within a terminal of your choice, set the two tokens from the previous step as environment variables using the commands below. Make sure not to mix these two up, `SLACK_APP_TOKEN` will start with “xapp-“ and `SLACK_BOT_TOKEN` will start with “xoxb-“.

```bash
export SLACK_APP_TOKEN=<YOUR-APP-TOKEN-HERE>
export SLACK_BOT_TOKEN=<YOUR-BOT-TOKEN-HERE>
```

Run the following commands to activate a virtual environment for your Python packages to be installed, install the dependencies, and start your app.

```bash
# Setup your python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Start your local server
python3 app.py
```

Now that your app is running, you should be able to see it within Slack. In Slack, create a channel that you can test in and try inviting your bot to it using the `/invite @Your-app-name-here` command. Check that your app works by saying “hi” in the channel where your app is, and you should receive a message back from it. If you don’t, ensure you completed all the steps above.

## Coding the app

There will be four major steps needed to get from the template to the finish line:

1. Update the “hi” message to something more interesting and interactive
2. Handle when the wrong delivery ID button is pressed
3. Handle when the correct delivery IDs are sent and bring up a modal for more information
4. Send the information to all of the places needed when the form is submitted (including third-party locations)

All of these steps require you to use [Block Kit Builder](https://app.slack.com/block-kit-builder), a tool that helps you create messages, modals and other surfaces within Slack. Open [Block Kit Builder](https://app.slack.com/block-kit-builder), take a look and play around! We’ll create some views next.

### Updating the "hi" message

The first thing we want to do is change the “hi, how are you?” message from our app into something more useful. Here’s something that you can use to start off with, but you can make it your own within Block Kit Builder. Once you have something you like, copy the blocks by clicking the **Copy Payload** button in the top right.

Take the function below and place your blocks within the blocks dictionary `[]`.  Update the payload: 
* Remove the initial blocks key and convert any boolean true values to `True` to fit with Python conventions.
* If you see variables within `{}` brackets, this is part of an f-string, which allows you to insert variables within strings in a clean manner. Place the `f` character before these strings like this:

```python
{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": f"Confirm *{delivery_id}* is correct?", # place the "f" character here at the beginning of the string
    },
},
```

Place all of this in the `sample_message.py` file.

```python
def delivery_message_callback(context: BoltContext, say: Say, logger: Logger):
    try:
        delivery_id = context["matches"][0]
        say( 
            blocks=[] # insert your blocks here
        )
    except Exception as e:
        logger.error(e)
```

Next, you’ll need to make some connections so that this function is called when a message is sent in the channel where your app is. Head to `messages/__init__.py` and add the line below to the register function. Don’t forget to add the import to the callback function as well!

```python

from .sample_message import delivery_message_callback ## import the function to this file

def register(app: App):
    app.message(re.compile("(hi|hello|hey)"))(sample_message_callback) # This can be deleted!
    # This regex will capture any number letters followed by dash 
    # and then any number of digits, our "confirmation number" e.g. ASDF-1234
    app.message(re.compile(r"[A-Za-z]+-\d+"))(delivery_message_callback) ## add this line!

```

Now, restart your server to bring in the new code and test that your function works by sending an order confirmation ID, like `HWOA-1524`, in your testing channel. Your app should respond with the message you created within Block Kit Builder.

## Handling an incorrect delivery ID

Notice that if you try to click on either of the buttons within your message, nothing will happen. This is because we have yet to create a function to handle the button click. Let’s start with the `Not correct` button first.

1. Head to Block Kit Builder once again. We want to build a message that lets the user know that the wrong order ID has been submitted. Here's [something to get you started](https://app.slack.com/block-kit-builder/#%7B%22blocks%22:%5B%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22Delivery%20*%7Bdelivery_id%7D*%20was%20incorrect%20%E2%9D%8C%22%7D%7D%5D%7D).

2. Once you have something that you like, add it to the function below and place the function within the `actions/sample_action.py` file. Remember to make any strings with variables into f-strings!

```python
def deny_delivery_callback(ack, body, client, logger: Logger):
    try:
        ack()
        delivery_id = body["message"]["text"].split("*")[1]

        # Calls the chat.update function to replace the message, 
        # preventing it from being pressed more than once.
        client.chat_update(
            channel=body["container"]["channel_id"],
            ts=body["container"]["message_ts"],
            blocks=[], # Add your blocks here!
        )

        logger.info(f"Delivery denied by user {body['user']['id']}")
    except Exception as e:
        logger.error(e)
```

This function will call the [`chat.update`](/methods/chat.update) Web API method, which will update the original message with buttons, to the one that we created previously. This will also prevent the message from being pressed more than once.

3. Make the connection to this function again within the `actions/__init__.py` folder with the following code:

```python

from slack_bolt import App
from .sample_action import sample_action_callback # This can be deleted
from .sample_action import deny_delivery_callback

def register(app: App):
    app.action("sample_action_id")(sample_action_callback) # This can be deleted
    app.action("deny_delivery")(deny_delivery_callback) # Add this line

```

Test out your code by sending in a confirmation number into your channel and clicking the `Not correct` button. If the message is updated, then you’re good to go onto the next step.

## Handling a correct delivery ID

The next step is to handle the `Confirm` button. In this case, we’re going to pull up a modal instead of just a message.

1. Using the following [modal](https://app.slack.com/block-kit-builder/#%7B%22type%22:%22modal%22,%22callback_id%22:%22approve_delivery_view%22,%22title%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Approve%20Delivery%22%7D,%22private_metadata%22:%22%7Bdelivery_id%7D%22,%22blocks%22:%5B%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22Approving%20delivery%20*%7Bdelivery_id%7D*%22%7D%7D,%7B%22type%22:%22input%22,%22block_id%22:%22notes%22,%22label%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Additional%20delivery%20notes%22%7D,%22element%22:%7B%22type%22:%22plain_text_input%22,%22action_id%22:%22notes_input%22,%22multiline%22:true,%22placeholder%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Add%20notes...%22%7D%7D,%22optional%22:true%7D,%7B%22type%22:%22input%22,%22block_id%22:%22location%22,%22label%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Delivery%20Location%22%7D,%22element%22:%7B%22type%22:%22plain_text_input%22,%22action_id%22:%22location_input%22,%22placeholder%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Enter%20the%20location%20details...%22%7D%7D,%22optional%22:true%7D,%7B%22type%22:%22input%22,%22block_id%22:%22channel%22,%22label%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Notification%20Channel%22%7D,%22element%22:%7B%22type%22:%22channels_select%22,%22action_id%22:%22channel_select%22,%22placeholder%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Select%20channel%20for%20notifications%22%7D%7D,%22optional%22:false%7D%5D,%22submit%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Approve%22%7D%7D) as a base, create a modal that captures the kind of information that you need.

2. Within the `actions/sample_action.pyfile`, add the following function, replacing the view with the one you created above. Again, any strings with variables will be updated to f-strings and also any booleans will need to be capitalized.

```python

def approve_delivery_callback(ack, body, client, logger: Logger):
    try:
        ack()

        delivery_id = body["message"]["text"].split("*")[1]
        # Updates the original message so you can't press it twice
        client.chat_update(
            channel=body["container"]["channel_id"],
            ts=body["container"]["message_ts"],
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Processed delivery *{delivery_id}*...",
                    },
                }
            ],
        )

        # Open a modal to gather information from the user
        client.views_open(
            trigger_id=body["trigger_id"],
            view={} # Add your view here
        )

        logger.info(f"Approval modal opened by user {body['user']['id']}")
    except Exception as e:
        logger.error(e)

```

Similar to the `deny` button, we need to hook up all the connections.  Your `actions/__init__.py` should look something like this:

```python

from slack_bolt import App
from .sample_action import deny_delivery_callback
from .sample_action import approve_delivery_callback


def register(app: App):
    app.action("approve_delivery")(approve_delivery_callback)
    app.action("deny_delivery")(deny_delivery_callback)

```

Test your app by typing in a confirmation number in channel, click the confirm button and see if the modal comes up and you are able to capture information from the user.

## Submitting the form

Lastly, we’ll handle the submission of the form, which will trigger two things. We want to send the information into the specified channel, which will let the user know that the form was successful, as well as send the information into our system of record, Salesforce.

1. Here’s a [simple example](https://app.slack.com/block-kit-builder/?1#%7B%22blocks%22:%5B%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22%E2%9C%85%20Delivery%20*%7Bdelivery_id%7D*%20approved:%22%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Delivery%20Notes:*%5Cn%7Bnotes%20or%20'None'%7D%22%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Delivery%20Location:*%5Cn%7Bloc%20or%20'None'%7D%22%7D%7D%5D%7D) of a message that you can use to present the information in channel. Modify it however you like and then place it within the code below in the `/views/sample_views.py` file.

```python

def handle_approve_delivery_view(ack, client, view, logger: Logger):
    try:
        ack()

        delivery_id = view["private_metadata"]
        values = view["state"]["values"]
        notes = values["notes"]["notes_input"]["value"]
        loc = values["location"]["location_input"]["value"]
        channel = values["channel"]["channel_select"]["selected_channel"]

        client.chat_postMessage(
            channel=channel,
            blocks=[], ## Add your message here
        )

    except Exception as e:
        logger.error(f"Error in approve_delivery_view: {e}")

```

2. Making the connections in the `/views/__init__.py `file, we can test that this works by sending a message once again in our test channel.

```python

from slack_bolt import App
from .sample_view import handle_approve_delivery_view

def register(app: App):
    app.view("sample_view_id")(sample_view_callback) # This can be deleted
    app.view("approve_delivery_view")(handle_approve_delivery_view) ## Add this line

```

3. Let’s also send the information to Salesforce. There are [several ways](https://github.com/simple-salesforce/simple-salesforce?tab=readme-ov-file#examples) for you to access Salesforce through its API, but in this workshop, we’ve utilized `username`, `password` and `token`. If you need help with getting your API token for Salesforce, take a look at [this article](https://help.salesforce.com/s/articleView?id=xcloud.user_security_token.htm&type=5). You’ll need to add these values as environment variables like we did earlier with our Slack tokens. You can use the following commands:

```bash

export SF_USERNAME=<YOUR-USERNAME>
export SF_PASSWORD=<YOUR-PASSWORD>
export SF_TOKEN=<YOUR-SFDC-TOKEN>

```

4. We’re going to use assume that order information is stored in the Order object and that the confirmation IDs map to the 8-digit Order numbers within Salesforce. Given that assumption, all we need to do is make a query to find the correct object, add the inputted information, and we’re done. Place this code before the last except within the `/views/sample_views.py` file.

```python

# Extract just the numeric portion from delivery_id
        delivery_number = "".join(filter(str.isdigit, delivery_id))

        # Update Salesforce order object
        try:
            sf = Salesforce(
                username=os.environ.get("SF_USERNAME"),
                password=os.environ.get("SF_PASSWORD"),
                security_token=os.environ.get("SF_TOKEN"),
            )

            # Assuming delivery_id maps to Salesforce Order number
            order = sf.query(f"SELECT Id FROM Order WHERE OrderNumber = '{delivery_number}'")  # noqa: E501
            if order["records"]:
                order_id = order["records"][0]["Id"]
                sf.Order.update(
                    order_id,
                    {
                        "Status": "Delivered",
                        "Description": notes,
                        "Shipping_Location__c": loc,
                    },
                )
                logger.info(f"Updated order {delivery_id}")
            else:
                logger.warning(f"No order found for {delivery_id}")

        except Exception as sf_error:
            logger.error(f"Update failed for order {delivery_id}: {sf_error}")
            # Continue execution even if Salesforce update fails

```

You’ll also need to add the two imports that are found within this code to the top of the file.

```python
import os
from simple_salesforce import Salesforce
```

With these imports, add `simple_salesforce` to your `requirements.txt` file, then install that package with the following command once again.

```bash
pip install -r requirements.txt
```

## Testing your app

Test your app one last time, and you’re done!

Congratulations! You’ve built an app using [Bolt for Python](/bolt-python/) that allows you to send information into Slack, as well as into a third-party service. While there are more features you can add to make this a more robust app, we hope that this serves as a good introduction into connecting services like Salesforce using Slack as a conduit.