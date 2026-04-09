---
sidebar_label: Quickstart
title: Quickstart guide with Bolt for Python
---

This quickstart guide aims to help you get a Slack app using Bolt for Python up and running as soon as possible!

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

When complete, you'll have a local environment configured with a customized [app](https://github.com/slack-samples/bolt-python-getting-started-app) running to modify and make your own.

:::tip[Reference for readers]

In search of the complete guide to building an app from scratch? Check out the [building an app](/tools/bolt-python/building-an-app) guide.

:::

#### Prerequisites

A few tools are needed for the following steps:
* A workspace where development can happen is also needed. We recommend using [developer sandboxes](/tools/developer-sandboxes) to avoid disruptions where real work gets done.
* Git
* [Python 3.7 or later](https://www.python.org/downloads/). Refer to [Python's setup and building guide](https://devguide.python.org/getting-started/setup-building/) for more details.


import QuickstartGuide from '@site/src/components/QuickstartGuide';

<QuickstartGuide 
  steps={[
    {
      number: 1,
      title: 'Install the Slack CLI',
      description: 'Download the command-line tool for developing Slack apps.',
      commands: {
        macos: 'curl -fsSL https://downloads.slack-edge.com/slack-cli/install.sh | bash',
        windows: 'irm https://downloads.slack-edge.com/slack-cli/install-windows.ps1 | iex'
      }
    },
    {
      number: 2,
      title: 'Connect to your workspace',
      description: 'Log in and authenticate with your Slack workspace.',
      commands: {
        macos: 'slack login',
        windows: 'slack login'
      }
    },
    {
      number: 3,
      title: 'Use Casey as a template',
      description: 'Create a project using the starter template sample app',
      commands: {
        macos: 'slack create first-slack-agent --template slack-samples/bolt-python-starter-template',
        windows: 'slack create first-slack-agent --template slack-samples/bolt-python-starter-template'
      }
    }
  ]}
/>


You now have the Slack CLI and the starter sample app ready for use. Open up the app in your editor of choice and let's explore what the agent can actually do.


## Setting up your environment

After the project is created you'll have a `requirements.txt` file for app dependencies and a `.slack` directory for Slack CLI configuration.

A few other files exist too, but we'll visit these later.

We recommend using a [Python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) to manage your project's dependencies. This is a great way to prevent conflicts with your system's Python packages. Let's create and activate a new virtual environment with [Python 3.7 or later](https://www.python.org/downloads/):

```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Confirm the virtual environment is active by checking that the path to `python3` is _inside_ your project ([a similar command is available on Windows](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)):

```sh
$ which python3
# Output: /path/to/first-bolt-app/.venv/bin/python3
```

## Running the app {#running-the-app}

Before you can start developing with Bolt, you will want a running Slack app.

The getting started app template contains a `manifest.json` file with details about an app that we will use to get started. Use the following command and select "Create a new app" to install the app to the team of choice:

```sh
$ slack run
...
⚡️ Bolt app is running!
```

With the app running, you can test it out with the following steps in Slack:

1. Open a direct message with your app or invite the bot `@first-bolt-app (local)` to a public channel.
2. Send "hello" to the current conversation and wait for a response.
3. Click the attached button labelled "Click Me" to post another reply.

After confirming the app responds, celebrate, then interrupt the process by pressing `CTRL+C` in the terminal to stop your app from running.

## Updating the app

At this point, you've successfully run the getting started Bolt for Python [app](https://github.com/slack-samples/bolt-python-getting-started-app)!

The defaults included leave opportunities abound, so to personalize this app let's now edit the code to respond with a kind farewell.

#### Responding to a farewell

Chat is a common thing apps do and responding to various types of messages can make conversations more interesting.

Using an editor of choice, open the `app.py` file and add the following import to the top of the file, and message listener after the "hello" handler:

```python
import random

@app.message("goodbye")
def message_goodbye(say):
    responses = ["Adios", "Au revoir", "Farewell"]
    parting = random.choice(responses)
    say(f"{parting}!")
```

Once the file is updated, save the changes and then we'll make sure those changes are being used.

Run the following command and select the app created earlier to start, or restart, your app with the latest changes:

```sh
$ slack run
...
⚡️ Bolt app is running!
```

After finding the above output appears, open Slack to perform these steps:

1. Return to the direct message or public channel with your bot.
2. Send "goodbye" to the conversation.
3. Receive a parting response from before and repeat "goodbye" to find another one.

Your app can be stopped again by pressing `CTRL+C` in the terminal to end these chats.

#### Customizing app settings

The created app will have some placeholder values and a small set of [scopes](/reference/scopes) to start, but we recommend exploring the customizations possible on app settings.

Open app settings for your app with the following command:

```sh
$ slack app settings
```

This will open the following page in a web browser:

![Basic Information page](/img/bolt-python/basic-information-page.png "Basic Information page")

On these pages you're free to make changes such as updating your app icon, configuring app features, and perhaps even distributing your app!

## Next steps {#next-steps}

You can now continue customizing your app with various features to make it right for whatever job's at hand. Here are some ideas about what to explore next:

- Follow along with the steps that went into making this app on the [building an app](/tools/bolt-python/building-an-app) guide for an educational overview.
- Check out the [Agent quickstart](/ai/agent-quickstart) to get up and running with an agent.
- Browse our [curated catalog of samples](/samples) for more apps to develop off of.