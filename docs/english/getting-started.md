---
sidebar_label: Quickstart
title: Quickstart guide with Bolt for Python
---

This quickstart guide aims to help you get a Slack app using Bolt for Python up and running as soon as possible! 

When complete, you'll have a local environment configured with a customized [app](https://github.com/slack-samples/bolt-python-getting-started-app) that responds to "hello" messages. You'll then be able to modify it and make it your own.

## Setting up the app

:::info[A workspace where development can happen is needed.]

We recommend using [developer sandboxes](/tools/developer-sandboxes) to avoid disruptions where real work gets done.

:::

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
      title: 'Use the starter app as a template',
      description: 'Select "Starter app" after running the command',
      commands: {
        macos: 'slack create',
        windows: 'slack create'
      }
    },
    {
      number: 4,
      title: 'Run your app',
      description: 'See your app working in Slack.',
      commands: {
        macos: 'slack run',
        windows: 'slack run'
      }
    }
  ]}
  buttonText="View app code"
  buttonLink="https://github.com/slack-samples/bolt-python-getting-started-app"
  buttonIcon={true}
/>

## Testing the app {#testing-the-app}

With the app running, you can test it out with the following steps in Slack:

1. Invite the bot `@first-bolt-app (local)` to a public channel. You can do this a few ways:
    Option A: @-mention them in a message in a channel. You will be prompted to add them
    Option B: Click the channel name, go to the "Integrations" tab, and click the "Add apps" button 
    
2. Send "hello" to the current conversation and wait for a response.

After confirming the app responds, celebrate, then interrupt the process by pressing `CTRL+C` in the terminal to stop your app from running.

## Updating the app

At this point, you've successfully run the getting started Bolt for Python [app](https://github.com/slack-samples/bolt-python-getting-started-app)!

The defaults included leave opportunities abound, so to personalize this app let's now edit the code to respond with a kind farewell.

### Responding to a farewell

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

### Customizing app settings

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

- Learn the steps that went into making this app on the [creating an app](/tools/bolt-python/creating-an-app) guide for an educational overview. This is also where you can learn how to create the app without using the Slack CLI.
- Check out the [Agent quickstart](/ai/agent-quickstart) to get up and running with an agent.
- Browse our [curated catalog of samples](/samples) for more apps to use as a starting point for development.