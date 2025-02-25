# Modals

If you're learning about Slack apps, modals, or slash commands for the first time, you've come to the right place! In this tutorial, we'll take a look at setting up your very own server using Glitch, and using that server to run your Slack app. 

Let's take a look at the technologies we'll use in this tutorial:

* Glitch is a online IDE that allows you to collaboratively work on code and host your own server. Glitch should only be used for development purposes and should not be used in production.
* We'll use Python in conjunction with our [Bolt for Python](https://github.com/SlackAPI/bolt-python) SDK.
* [Block Kit](https://api.slack.com/block-kit/building) is a UI framework for Slack apps that allows you to create beautiful, interactive messages within Slack. If you've ever seen a message in Slack with buttons or a select menu, that's Block Kit.
* Modals are similar to a pop-up window that displays right in Slack. They grab the attention of the user, and are normally used to prompt users to provide some kind of information or input.

---

## Final product overview {#final_product}
If you follow through with the extra credit tasks, your final app will look like this:

![Final product](/img/tutorials/modals/final_product.gif)

---

## The process {#steps}

1. [Create a new app](https://api.slack.com/apps/new) and name it whatever you like.

2. [Remix (or clone)](https://glitch.com/edit/#!/remix/intro-to-modals-bolt) the Glitch template.

Here's a copy of what the modal payload looks like &mdash; this is what powers the modal.

```json
{
  "type": "modal",
  "callback_id": "gratitude-modal",
  "title": {
    "type": "plain_text",
    "text": "Gratitude Box",
    "emoji": true
  },
  "submit": {
    "type": "plain_text",
    "text": "Submit",
    "emoji": true
  },
  "close": {
    "type": "plain_text",
    "text": "Cancel",
    "emoji": true
  },
  "blocks": [
    {
      "type": "input",
      "block_id": "my_block",
      "element": {
        "type": "plain_text_input",
        "action_id": "my_action"
      },
      "label": {
        "type": "plain_text",
        "text": "Say something nice!",
        "emoji": true
      }
    }
  ]
}
```

3. Find the base path to your server by clicking **Share**, then copy the Live site link.

	![Get the base link](/img/tutorials/modals/base_link.gif)

4. On your app page, navigate to **Interactivity & Shortcuts**. Append "/slack/events" to your base path URL and enter it into the **Request URL** e.g., `https://festive-harmonious-march.glitch.me/slack/events`.  This allows your server to retrieve information from the modal. You can see the code for this within the Glitch project.

	![Interactivity URL](/img/tutorials/modals/interactivity_url.png)

5. Create the slash command so you can access it within Slack. Navigate to the **Slash Commands** section and create a new command. Note the **Request URL** is the same link as above, e.g. `https://festive-harmonious-march.glitch.me/slack/events` . The code that powers the slash command and opens a modal can be found within the Glitch project.

	![Slash command details](/img/tutorials/modals/slash_command.png)

6. Select **Install App**. After you've done this, you'll see a **Bot User OAuth Access Token**, copy this.

7. Navigate to your Glitch project and click the `.env` file where the credentials are stored, and paste your bot token where the `SLACK_BOT_TOKEN` variable is shown. This allows your server to send authenticated requests to the Slack API. You'll also need to head to your app's settings page under **Basic Information** and copy the _Signing secret_ to place into the `SLACK_SIGNING_SECRET` variable. 

	![Environment variables](/img/tutorials/modals/heart_icon.gif)

8. Test by heading to Slack and typing `/thankyou`.

All done! 🎉 You've created your first slash command using Block Kit and modals! The world is your oyster; you can create more complex modals by playing around with [Block Kit Builder](https://app.slack.com/block-kit-builder).

### Extra credit {#extra_credit}

For a little extra credit, let's post the feedback we received in a channel.

1. Add the `chat:write` bot scope, which allows your bot to post messages within Slack. You can do this in the **OAuth & Permissions** section for your Slack app.  
2. Reinstall your app to apply the scope.
3. Create a channel and name it `#thanks`.  Get its ID by right clicking the channel name, copying the link, and copying the last part starting with the letter `C`. For example, if your channel link looks like this: https://my.slack.com/archives/C123FCN2MLM, the ID is `C123FCN2MLM`. 
4. Add your bot to the channel by typing the command `/invite @your_bots_name`.
5. Uncomment the `Extra Credit` code within your Glitch project and make sure to replace `your_channel_id` with the ID above.
6. Test it out by typing `/thankyou`, and watching all the feedback come into your channel!

## Next steps {#next-steps}

If you want to learn more about Bolt for Python, refer to the [Getting Started guide](/bolt-python/getting-started).
