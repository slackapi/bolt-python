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

![OAuth Tokens](../assets/bot-token.png "Bot OAuth Token")

> 💡 Treat your token like a password and [keep it safe](https://api.slack.com/docs/oauth-safety). Your app uses it to post and retrieve information from Slack workspaces.