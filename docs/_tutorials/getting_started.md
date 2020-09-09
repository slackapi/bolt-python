---
title: Getting started
order: 0
slug: getting-started
lang: en
layout: tutorial
permalink: /tutorial/getting-started
redirect_from:
  - /getting-started
---
# Getting started with Bolt for Python

<div class="section-content">
This guide is meant to walk you through getting up and running with a Slack app using Bolt for Python. Along the way, we’ll create a new Slack app, set up your local environment, and develop an app that listens and responds to messages from a Slack workspace.
</div> 

---

### Create an app
First thing's first: before you start developing with Bolt, you'll want to [create a Slack app](https://api.slack.com/apps/new). 

> 💡 We recommend using a workspace where you won't disrupt real work getting done — [you can create a new one for free](https://slack.com/get-started#create).

After you fill out an app name (_you can change it later_) and pick a workspace to install it to, hit the `Create App` button and you'll land on your app's **Basic Information** page.

This page contains an overview of your app in addition to important credentials you'll need later, like the `Signing Secret` under the **App Credentials** header. 

<!--TODO - Update image to match the latest App Directory sidebar (but remove the Workflows beta) -->
![Basic Information page](../assets/basic-information-page.png "Basic Information page")

Look around, add an app icon and description, and then let's start configuring your app 🔩

---

### Tokens and installing apps
Slack apps use [OAuth to manage access to Slack's APIs](https://api.slack.com/docs/oauth). When an app is installed, you'll receive a token that the app can use to call API methods. 

There are two token types available to a Slack app: user (`xoxp`) and bot (`xoxb`) tokens. User tokens allow you to call API methods on behalf of users after they install or authenticate the app. There may be several user tokens for a single workspace. Bot tokens are associated with bot users, and are only granted once in a workspace where someone installs the app. The bot token your app uses will be the same no matter which user performed the installation. Bot tokens are the token type that _most_ apps use.

For brevity, we're going to use bot tokens for this guide.

Navigate to the **OAuth & Permissions** on the left sidebar and scroll down to the **Bot Token Scopes** section. Click **Add an OAuth Scope**.

For now, we'll just add one scope: [`chat:write`](https://api.slack.com/scopes/chat:write). This grants your app the permission to post messages in channels it's a member of.

Scroll up to the top of the OAuth & Permissions page and click **Install App to Workspace**. You'll be led through Slack's OAuth UI, where you should allow your app to be installed to your development workspace.

Once you authorize the installation, you'll land on the **OAuth & Permissions** page and see a **Bot User OAuth Access Token**.

<!--TODO - Update image to match the latest App Directory sidebar (but remove the Workflows beta) -->
![OAuth Tokens](../assets/bot-token.png "Bot OAuth Token")

> 💡 Treat your token like a password and [keep it safe](https://api.slack.com/docs/oauth-safety). Your app uses it to post and retrieve information from Slack workspaces.

---

### Setting up your local project
With the initial configuration handled, it's time to set up a new Bolt project. This is where you'll write the code that handles the logic for your app.

If you don’t already have a project, let’s create a new one. Create an empty directory:

```shell
mkdir first-bolt-app
cd first-bolt-app
```

Next, we recommend using a Python virtual environment to manage your project's dependencies. Create and activate a new virtual environment:

<!-- TODO - Details on installing Python version manager, virtual environment, adding it to the git ignore, etc -->
<!-- TODO - Do we use python or python3? -->
<!-- TODO - Should we confirm that the virtual environment is active? -->
```shell
python3 -m venv env
source env/bin/activate
```

Before we install the Bolt for Python package to your new project, let's save the bot token and signing secret that was generated when you configured your app. These should be stored as environment variables and should *not* be saved in version control.

1. **Copy your Signing Secret from the Basic Information page** and then store it in a new environment variable. The following example works on Linux and MacOS; but [similar commands are available on Windows](https://superuser.com/questions/212150/how-to-set-env-variable-in-windows-cmd-line/212153#212153).

```shell
export SLACK_SIGNING_SECRET=<your-signing-secret>
```

2. **Copy your bot (xoxb) token from the OAuth & Permissions page** and store it in another environment variable.

```shell
export SLACK_BOT_TOKEN=xoxb-<your-bot-token>
```

<!-- TODO - Is `slack_bolt` called a package in Python? -->
Now, lets create your app. Install the `slack_bolt` package to your virtual environment using the following command:

```shell
pip install slack_bolt
```
<!-- TODO - Do we want to mention that it will be installed to env/.../site-packages? -->

Create a new file called `app.py` in this directory and add the following code:

<!-- TODO - Is it best practice to separate imports and froms with a new line? -->
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

Your token and signing secret are enough to create your first Bolt app. Save your `app.py` file then on the command line run the following:

<!-- TODO - Should we make a note that there is no need to use python3 after init a virtual environment? -->
```script
python app.py
```

Your app should let you know that it's up and running.