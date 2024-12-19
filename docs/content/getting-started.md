---
title: Getting started with Bolt for Python
sidebar_label: Getting started
slug: getting-started
lang: en
---

This guide is meant to walk you through getting up and running with a Slack app using Bolt for Python. Along the way, we’ll create a new Slack app, set up your local environment, and develop an app that listens and responds to messages from a Slack workspace.

When you're finished, you'll have this ⚡️[Getting Started with Slack app](https://github.com/slackapi/bolt-python/tree/main/examples/getting_started) to run, modify, and make your own.
 
---

## Create an app {#create-an-app}

Before you start developing with Bolt, you'll want to [create a Slack app](https://api.slack.com/apps/new).

:::tip  

We recommend using a workspace where you won't disrupt real work getting done. Join the [Developer Program](https://api.slack.com/developer-program) and provision a sandbox with access to all Slack features for free.

:::

After you fill out an app name (_you can change it later_) and pick a workspace to install it to, hit the `Create App` button and you'll land on your app's **Basic Information** page.

This page contains an overview of your app in addition to important credentials you'll want to reference later. 

![Basic Information page](/img/boltpy/basic-information-page.png "Basic Information page")

Look around, add an app icon and description, and then let's start configuring your app 🔩

---

## Tokens and installing apps {#tokens-and-installing-apps}

Slack apps use [OAuth to manage access to Slack's APIs](https://api.slack.com/docs/oauth). When an app is installed, you'll receive a token that the app can use to call API methods.

There are three main token types available to a Slack app: user (`xoxp`), bot (`xoxb`), and app-level (`xapp`) tokens. 
- [User tokens](https://api.slack.com/authentication/token-types#user) allow you to call API methods on behalf of users after they install or authenticate the app. There may be several user tokens for a single workspace. 
- [Bot tokens](https://api.slack.com/authentication/token-types#bot) are associated with bot users, and are only granted once in a workspace where someone installs the app. The bot token your app uses will be the same no matter which user performed the installation. Bot tokens are the token type that _most_ apps use.
- [App-level tokens](https://api.slack.com/authentication/token-types#app) represent your app across organizations, including installations by all individual users on all workspaces in a given organization and are commonly used for creating WebSocket connections to your app.

We're going to use bot tokens for this guide.

1. Navigate to the **OAuth & Permissions** on the left sidebar and scroll down to the **Bot Token Scopes** section. Click **Add an OAuth Scope**.

2. For now, we'll just add one scope: [`chat:write`](https://api.slack.com/scopes/chat:write). This grants your app the permission to post messages in channels it's a member of.

3. Scroll up to the top of the **OAuth & Permissions** page and click **Install App to Workspace**. You'll be led through Slack's OAuth UI, where you should allow your app to be installed to your development workspace.

4. Once you authorize the installation, you'll land on the **OAuth & Permissions** page and see a **Bot User OAuth Access Token**. Save it for later.

![OAuth Tokens](/img/boltpy/bot-token.png "Bot OAuth Token")

:::info

Treat your token like a password and [keep it safe](https://api.slack.com/docs/oauth-safety). Your app uses it to post and retrieve information from Slack workspaces.

:::

### Using Socket Mode or HTTP

To listen for events happening in a Slack workspace (like when a message is posted or when a reaction is posted to a message) you'll use the [Events API to subscribe to event types](https://api.slack.com/events-api).

For those just starting, we recommend using [Socket Mode](https://api.slack.com/apis/connections/socket). Socket Mode allows your app to use the Events API and interactive features without exposing a public HTTP Request URL. This can be helpful during development, or if you're receiving requests from behind a firewall. 

That being said, you're welcome to set up an app with a public HTTP Request URL. HTTP is more useful for apps being deployed to hosting environments (like [AWS](/deployments/aws-lambda) or [Heroku](/deployments/heroku) to stably respond within a large corporate Slack workspaces/organization, or apps intended for distribution via the Slack Marketplace.

We've provided instructions for both ways in this guide.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs groupId="socket-or-http">
<TabItem value="socket-mode" label="Socket Mode">

If you're using Socket Mode, you'll also need an app-level token. 

Head over to **Basic Information** and scroll down under the App Token section and click **Generate Token and Scopes** to generate an app-level token. Add the `connections:write` scope to this token and save the generated `xapp` token — you'll need it for later.

</TabItem>
<TabItem value="http" label="HTTP">

If you're using HTTP, you'll also need a _signing secret_ that was generated when you configured your app. 

Head over to **Basic Information** and save your _signing Secret_ — you'll need it for later.

</TabItem>
</Tabs>

## Setting up your project {#setting-up-your-project}
With the initial configuration handled, it's time to set up a new Bolt project. This is where you'll write the code that handles the logic for your app.

If you don’t already have a project, let’s create a new one. Create an empty directory:

```shell
mkdir first-bolt-app
cd first-bolt-app
```

Next, we recommend using a [Python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) to manage your project's dependencies. This is a great way to prevent conflicts with your system's Python packages. Let's create and activate a new virtual environment with [Python 3.6 or later](https://www.python.org/downloads/):

```shell
python3 -m venv .venv
source .venv/bin/activate
```

We can confirm that the virtual environment is active by checking that the path to `python3` is _inside_ your project ([a similar command is available on Windows](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)):

```shell
which python3
# Output: /path/to/first-bolt-app/.venv/bin/python3
```

Copy your _bot (xoxb) token_ from the **OAuth & Permissions** page and store it as a new environment variable.

```shell
export SLACK_BOT_TOKEN=<xoxb-your-bot-token>
```

<Tabs groupId="socket-or-http">
<TabItem value="socket-mode" label="Socket Mode">

Store your _app-level (xapp) token_ as a new environment variable. 

```shell
export SLACK_APP_TOKEN=<your-app-level-token>
```

</TabItem>
<TabItem value="http" label="HTTP">

Store your _signing secret_ as a new environment variable.

```shell
export SLACK_SIGNING_SECRET=<your-signing-secret>
```

</TabItem>
</Tabs>

:::warning

Keep all tokens secure. At a minimum, you should avoid checking them into public version control, and access them via environment variables as we've done above. Checkout the API documentation for more on [best practices for app security](https://api.slack.com/authentication/best-practices).

:::

Now, let's create your app. Install the `slack_bolt` Python package to your virtual environment using the following command:

```shell
pip install slack_bolt
```

Create a new file called `app.py` in this directory and add the following code:

<Tabs groupId="socket-or-http">
<TabItem value="socket-mode" label="Socket Mode">

```python
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

</TabItem>
<TabItem value="http" label="HTTP">

```python
import os
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
```

</TabItem>
</Tabs>

Save your `app.py` file then on the command line run the following:

```script
python3 app.py
```

Your app should let you know that it's up and running. 🎉

---

## Setting up events {#setting-up-events}

Your app behaves similarly to people on your team — it can post messages, add emoji reactions, and listen and respond to events. It's time to tell Slack what events we'd like to listen for.

When an event occurs, Slack will send your app some information about the event, like the user that triggered it and the channel it occurred in. Your app will process the details and can respond accordingly.

Let's enable events for your app.

<Tabs groupId="socket-or-http">
<TabItem value="socket-mode" label="Socket Mode">

1. Head to your app's app settings page (click on the app [from the app settings page](https://api.slack.com/apps)). Navigate to **Socket Mode** on the left side menu and toggle to enable.

2. Go to **Basic Information** and scroll down under the App Token section and click **Generate Token and Scopes** to generate an app token. Add the `connections:write` scope to this token and save the generated `xapp` token, we'll use that in just a moment.

3. Go to **Event Subscriptions** via the left sidebar. Toggle the switch labeled **Enable Events**.

</TabItem>
<TabItem value="http" label="HTTP">

1. Go to **Event Subscriptions** via the left sidebar. Toggle the switch labeled **Enable Events**.

2. Add your Request URL. Slack will send HTTP POST requests corresponding to events to this [Request URL](https://api.slack.com/apis/connections/events-api#the-events-api__subscribing-to-event-types__events-api-request-urls) endpoint. Bolt uses the `/slack/events` path to listen to all incoming requests (whether shortcuts, events, or interactivity payloads). When configuring your Request URL within your app configuration, you'll append `/slack/events`, e.g. `https://<your-domain>/slack/events`. 💡 As long as your Bolt app is still running, your URL should become verified.

:::info 

For local development, you can use a proxy service like [ngrok](https://ngrok.com/) to create a public URL and tunnel requests to your development environment. Refer to [ngrok's getting started guide](https://ngrok.com/docs#getting-started-expose) on how to create this tunnel.

:::

</TabItem>
</Tabs>

Under **Subscribe to Bot Events**, you can add events for your bot to respond to. There are four events related to messages:

- [`message.channels`](https://api.slack.com/events/message.channels) listens for messages in public channels that your app is added to
- [`message.groups`](https://api.slack.com/events/message.groups) listens for messages in 🔒 private channels that your app is added to
- [`message.im`](https://api.slack.com/events/message.im) listens for messages in your app's DMs with users
- [`message.mpim`](https://api.slack.com/events/message.mpim) listens for messages in multi-person DMs that your app is added to

If you want your bot to listen to messages from everywhere it is added to, choose all four message events. After you’ve selected the events you want your bot to listen to, click the green **Save Changes** button.

---

## Listening and responding to a message {#listening-and-responding-to-a-message}
Your app is now ready for some logic. Let's start by using the `message()` method to attach a listener for messages.

The following example listens and responds to all messages in channels/DMs where your app has been added that contain the word "hello":

<Tabs groupId="socket-or-http">
<TabItem value="socket-mode" label="Socket Mode">

```python
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

</TabItem>
<TabItem value="http" label="HTTP">

```python
import os
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
```

</TabItem>
</Tabs>

If you restart your app, so long as your bot user has been added to the channel/DM, when you send any message that contains "hello", it will respond.

This is a short example, but it gives you a place to start customizing your app based on your own goals. Let's try something a little more interactive by sending a button rather than plain text.

---

## Sending and responding to actions {#sending-and-responding-to-actions}

To use features like buttons, select menus, datepickers, modals, and shortcuts, you’ll need to enable interactivity. Head over to **Interactivity & Shortcuts** in your app settings.

<Tabs groupId="socket-or-http">
<TabItem value="socket-mode" label="Socket Mode">

With Socket Mode on, basic interactivity is enabled for us by default, so no further action here is needed

</TabItem>
<TabItem value="http" label="HTTP">

Similar to events, you'll need to specify a Request URL for Slack to send the action (such as *user clicked a button*).

By default, Bolt is configured to use the same endpoint for interactive components that it uses for events, so use the same request URL as above (for example, `https://8e8ec2d7.ngrok.io/slack/events`). Press the **Save Changes** button in the lower right hand corner. Your app is now set up to handle interactivity!

![Configuring a Request URL](/img/boltpy/request-url-config.png "Configuring a Request URL")

</TabItem>
</Tabs>

When interactivity is enabled, interactions with shortcuts, modals, or interactive components (such as buttons, select menus, and datepickers) will be sent to your app as events.

Now, let's go back to your app's code and add logic to handle those events:
- First, we'll send a message that contains an interactive component (in this case a button)
- Next, we'll listen for the action of a user clicking the button before responding

Below, the code from the last section is modified to send a message containing a button rather than just a string:

<Tabs groupId="socket-or-http">
<TabItem value="socket-mode" label="Socket Mode">

```python
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    # signing_secret=os.environ.get("SLACK_SIGNING_SECRET") # not required for socket mode
)

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

```

</TabItem>
<TabItem value="http" label="HTTP">

```python
import os
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
```

</TabItem>
</Tabs>

The value inside of `say()` is now an object that contains an array of `blocks`. Blocks are the building components of a Slack message and can range from text to images to datepickers. In this case, your app will respond with a section block that includes a button as an accessory. Since we're using `blocks`, the `text` is a fallback for notifications and accessibility.

You'll notice in the button `accessory` object, there is an `action_id`. This will act as a unique identifier for the button so your app can specify what action it wants to respond to.

:::tip  

The [Block Kit Builder](https://app.slack.com/block-kit-builder) is an simple way to prototype your interactive messages. The builder lets you (or anyone on your team) mockup messages and generates the corresponding JSON that you can paste directly in your app.

:::

Now, if you restart your app and say "hello" in a channel your app is in, you'll see a message with a button. But if you click the button, nothing happens (*yet!*).

Let's add a handler to send a followup message when someone clicks the button:

<Tabs groupId="socket-or-http">
<TabItem value="socket-mode" label="Socket Mode">

```python
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

</TabItem>
<TabItem value="http" label="HTTP">

```python
import os
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
```

</TabItem>
</Tabs>

You can see that we used `app.action()` to listen for the `action_id` that we named `button_click`. If you restart your app and click the button, you'll see a new message from your app that says you clicked the button.

---

## Next steps {#next-steps}

You just built your first [Bolt for Python app](https://github.com/slackapi/bolt-python/tree/main/examples/getting_started)!

Now that you have a basic app up and running, you can start exploring how to make your Bolt app stand out. Here are some ideas about what to explore next:

* Read through the site to learn about the different methods and features your Bolt app has access to.

* Explore the different events your bot can listen to with the [`app.event()`](/concepts/event-listening) method. All of the events are listed [on the API site](https://api.slack.com/events).

* Bolt allows you to [call Web API methods](/concepts/web-api) with the client attached to your app. There are [over 200 methods](https://api.slack.com/methods) on our API site.

* Learn more about the different token types [on our API site](https://api.slack.com/docs/token-types). Your app may need different tokens depending on the actions you want it to perform.