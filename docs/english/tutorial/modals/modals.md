# Modals

If you're learning about Slack apps, modals, or slash commands for the first time, you've come to the right place! In this tutorial, we'll take a look at setting up your very own server using GitHub Codespaces, then using that server to run your Slack app built with the [**Bolt for Python framework**](https://github.com/SlackAPI/bolt-python).

:::info[GitHub Codespaces]
GitHub Codespaces is an online IDE that allows you to work on code and host your own server at the same time. While Codespaces is good for testing and development purposes, it should not be used in production.

:::

At the end of this tutorial, your final app will look like this:

![announce](https://github.com/user-attachments/assets/0bf1c2f0-4b22-4c9c-98b3-b21e9bcc14a8)

And will make use of these Slack concepts:
* [**Block Kit**](/block-kit/) is a UI framework for Slack apps that allows you to create beautiful, interactive messages within Slack. If you've ever seen a message in Slack with buttons or a select menu, that's Block Kit.
* [**Modals**](/surfaces/modals) are a pop-up window that displays right in Slack. They grab the attention of the user, and are normally used to prompt users to provide some kind of information or input in a form.
* [**Slash Commands**](/interactivity/implementing-slash-commands) allow you to invoke your app within Slack by just typing into the message composer box. e.g. `/remind`, `/topic`.

If you're familiar with using Heroku you can also deploy directly to Heroku with the following button.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/wongjas/modal-example)

---

## Setting up your app within App Settings {#setting-up-app-settings}

You'll need to create an app and configure it properly within App Settings before using it.

1. [Create a new app](https://api.slack.com/apps/new), click `From a Manifest`, and choose the workspace that you want to develop on. Then copy the following JSON object; it describes the metadata about your app, like its name, its bot display name and permissions it will request.

```json
{
    "display_information": {
        "name": "Intro to Modals"
    },
    "features": {
        "bot_user": {
            "display_name": "Intro to Modals",
            "always_online": false
        },
        "slash_commands": [
            {
                "command": "/announce",
                "description": "Makes an announcement",
                "should_escape": false
            }
        ]
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "chat:write",
                "commands"
            ]
        }
    },
    "settings": {
        "interactivity": {
            "is_enabled": true
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": true,
        "token_rotation_enabled": false
    }
}
```

2. Once your app has been created, scroll down to `App-Level Tokens` and create a token that requests for the [`connections:write`](/reference/scopes/connections.write) scope, which allows you to use [Socket Mode](/apis/events-api/using-socket-mode), a secure way to develop on Slack through the use of WebSockets. Copy the value of your app token and keep it for safe-keeping.

3. Install your app by heading to `Install App` in the left sidebar. Hit `Allow`, which means you're agreeing to install your app with the permissions that it is requesting. Be sure to copy the token that you receive, and keep it somewhere secret and safe.

## Starting your Codespaces server {#starting-server}

1. Log into GitHub and head to this [repository](https://github.com/wongjas/modal-example).

2. Click the green `Code` button and hit the `Codespaces` tab and then `Create codespace on main`.  This will bring up a code editor within your browser so you can start coding.  

## Understanding the project files {#understanding-files}

Within the project you'll find a `manifest.json` file. This is a a configuration file used by Slack apps. With a manifest, you can create an app with a pre-defined configuration, or adjust the configuration of an existing app.

The `simple_modal_example.py` Python script contains the code that powers your app. If you're going to tinker with the app itself, take a look at the comments found within the `simple_modal_example.py` file!

The `requirements.txt` file contains the Python package dependencies needed to run this app.

:::info[This repo contains optional Heroku-specific configurations]

The `app.json` file defines your Heroku app configuration including environment variables and deployment settings, to allow your app to deploy with one click. `Procfile` is a Heroku-specific file that tells Heroku what command to run when starting your app — in this case a Python script would run as a `worker` process. If you aren't deploying to Heroku, you can ignore both these files.

:::

## Adding tokens {#adding-tokens}

1. Open a terminal up within the browser's editor. 

2. Grab the app and bot tokens that you kept safe. We're going to set them as environment variables.

```bash
export SLACK_APP_TOKEN=<YOUR-APP-TOKEN-HERE>
export SLACK_BOT_TOKEN=<YOUR-BOT-TOKEN-HERE>
```

## Running the app {#running-app}

1. Activate a virtual environment for your Python packages to be installed.

```bash
# Setup your python virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the dependencies from the `requirements.txt` file.


```bash
# Install the dependencies
pip install -r requirements.txt
```

3. Start your app using the `python3 simple_modal_example.py` command. 

```bash
# Start your local server
python3 simple_modal_example.py
```

4. Now that your app is running, you should be able to see it within Slack. Test this by heading to Slack and typing `/announce`.

All done! 🎉 You've created your first slash command using Block Kit and modals! The world is your oyster; play around with [Block Kit Builder](https://app.slack.com/block-kit-builder) and create more complex modals and place them in your code to see what happens!

## Next steps {#next-steps}

If you want to learn more about Bolt for Python, refer to the [Getting Started guide](https://docs.slack.dev/bolt-python/getting-started).