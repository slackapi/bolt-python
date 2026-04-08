# AI Chatbot

In this tutorial, you'll learn how to bring the power of AI into your Slack workspace using a chatbot called Bolty that uses Anthropic or OpenAI. Here's what we'll do with this sample app:

1. Create your app using the Slack CLI
2. Set up and run your local project
3. Create a workflow using Workflow Builder to summarize messages in conversations
4. Select your preferred API and model to customize Bolty's responses
5. Interact with Bolty via direct message, the `/ask-bolty` slash command, or by mentioning the app in conversations

Intrigued? First, grab your tools by following the three steps below.

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
      title: 'Create a project',
      description: 'Set up a new Bolt project from a starter template.',
      commands: {
        macos: 'slack create ai-chatbot --template slack-samples/bolt-python-ai-chatbot',
        windows: 'slack create ai-chatbot --template slack-samples/bolt-python-ai-chatbot'
      }
    }
  ]}
buttonText="View sample app"
  buttonLink="https://github.com/slack-samples/bolt-python-ai-chatbot"
  buttonIcon={true}
/>

<br/>

## Prerequisites {#prereqs}

You will also need the following:

- a development workspace where you have permissions to install apps. If you don’t have a workspace you can join the [Developer Program](https://api.slack.com/developer-program) and provision a sandbox with access to all Slack features for free.
- a development environment with [Python 3.7](https://www.python.org/downloads/) or later.
- an Anthropic or OpenAI account with sufficient credits, and in which you have generated a secret key.

### Obtaining and storing your environment variables {#environment-variables}

Before you'll be able to successfully run the app, you'll need to first obtain and set some environment variables.

#### Provider tokens {#provider-tokens}

Models from different AI providers are available if the corresponding environment variable is added as shown in the sections below.

<Tabs groupId="ai-providers">
<TabItem value="anthropic" label="Anthropic">

To interact with Anthropic models, navigate to your Anthropic account dashboard to [create an API key](https://console.anthropic.com/settings/keys), then export the key as follows:

```bash
export ANTHROPIC_API_KEY=<your-api-key>
```

</TabItem>
<TabItem value="Google Cloud Vertex AI" label="Google Cloud Vertex AI">

To use Google Cloud Vertex AI, [follow this quick start](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal#expandable-1) to create a project for sending requests to the Gemini API, then gather [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc) with the strategy to match your development environment.

Once your project and credentials are configured, export environment variables to select from Gemini models:

```bash
export VERTEX_AI_PROJECT_ID=<your-project-id>
export VERTEX_AI_LOCATION=<location-to-deploy-model>
```

The project location can be located under the **Region** on the [Vertex AI](https://console.cloud.google.com/vertex-ai) dashboard, as well as more details about available Gemini models.

</TabItem>
<TabItem value="OpenAI" label="OpenAI">

Unlock the OpenAI models from your OpenAI account dashboard by clicking [create a new secret key](https://platform.openai.com/api-keys), then export the key like so:

```bash
export OPENAI_API_KEY=<your-api-key>
```

</TabItem>
</tabs>

## Setting up and running your local project {#configure-project}


Start your Python virtual environment:

<Tabs groupId="os">
<TabItem value="macos" label="macOS">

```bash
python3 -m venv .venv
source .venv/bin/activate
```

</TabItem>
<TabItem value="windows" label="Windows">

```bash
py -m venv .venv
.venv\Scripts\activate
```

</TabItem>
</Tabs>

Install the required dependencies:

```bash
pip install -r requirements.txt
```

RUn your app locally:

```bash
slack run
```

If your app is indeed up and running, you'll see a message that says "⚡️ Bolt app is running!"

## Choosing your provider {#provider}

Navigate to the Bolty **App Home** and select a provider from the drop-down menu. The options listed will be dependent on which secret keys you added when setting your environment variables.

If you don't see Bolty listed under **Apps** in your workspace right away, never fear! You can mention **@Bolty** in a public channel to add the app, then navigate to your **App Home**.

![Choose your AI provider](6.png)

## Setting up your workflow {#workflow}

Within your development workspace, open Workflow Builder by clicking on your workspace name and then **Tools > Workflow Builder**. Select **New Workflow** > **Build Workflow**.

Click **Untitled Workflow** at the top to rename your workflow. For this tutorial, we'll call the workflow **Welcome to the channel**. Enter a description, such as _Summarizes channels for new members_, and click **Save**.

![Setting up a new workflow](1.png)

Select **Choose an event** under **Start the workflow...**, and then choose **When a person joins a channel**. Select the channel name from the drop-down menu and click **Save**.

![Start the workflow](2.png)

Under **Then, do these things**, click **Add steps** and complete the following:

1. Select **Messages** > **Send a message to a person**.
2. Under **Select a member**, choose **The user who joined the channel** from the drop-down menu.
3. Under **Add a message**, enter a short message, such as _Hi! Welcome to `{}The channel that the user joined`. Would you like a summary of the recent conversation?_ Note that the _`{}The channel that the user joined`_ is a variable; you can insert it by selecting **{}Insert a variable** at the bottom of the message text box.
4. Select the **Add Button** button, and name the button _Yes, give me a summary_. Click **Done**.

![Send a message](3.png)

We'll add two more steps under the **Then, do these things** section.

First, scroll to the bottom of the list of steps and choose **Custom**, then choose **Bolty** and **Bolty Custom Function**. In the **Channel** drop-down menu, select **Channel that the user joined**. Click **Save**.

![Bolty custom function](4.png)

For the final step, complete the following:

1. Choose **Messages** and then **Send a message to a person**. Under **Select a member**, choose **Person who clicked the button** from the drop-down menu.
2. Under **Add a message**, click **Insert a variable** and choose **`{}Summary`** under the **Bolty Custom Function** section in the list that appears. Click **Save**.

![Summary](5.png)

When finished, click **Finish Up**, then click **Publish** to make the workflow available in your workspace.

## Interacting with Bolty {#interact}

### Summarizing recent conversations {#summarize}

In order for Bolty to provide summaries of recent conversation in a channel, Bolty _must_ be a member of that channel.

1. Invite Bolty to a channel that you are able to leave and rejoin (for example, not the **#general** channel or a private channel someone else created) by mentioning the app in the channel — i.e., tagging **@Bolty** in the channel and sending your message.
2. Slackbot will prompt you to either invite Bolty to the channel, or do nothing. Click **Invite Them**. Now when new users join the channel, the workflow you just created will be kicked off.

To test this, leave the channel you just invited Bolty to and rejoin it. This will kick off your workflow and you'll receive a direct message from **Welcome to the channel**. Click the **Yes, give me a summary** button, and Bolty will summarize the recent conversations in the channel you joined.

![Channel summary](7.png)

The central part of this functionality is shown in the following code snippet. Note the use of the [`user_context`](/tools/deno-slack-sdk/reference/slack-types#usercontext) object, a Slack type that represents the user who is interacting with our workflow, as well as the `history` of the channel that will be summarized, which includes the ten most recent messages.

```python
from ai.providers import get_provider_response
from logging import Logger
from slack_bolt import Complete, Fail, Ack
from slack_sdk import WebClient
from ..listener_utils.listener_constants import SUMMARIZE_CHANNEL_WORKFLOW
from ..listener_utils.parse_conversation import parse_conversation

"""
Handles the event to summarize a Slack channel's conversation history.
It retrieves the conversation history, parses it, generates a summary using an AI response,
and completes the workflow with the summary or fails if an error occurs.
"""

def handle_summary_function_callback(
    ack: Ack, inputs: dict, fail: Fail, logger: Logger, client: WebClient, complete: Complete
):
    ack()
    try:
        user_context = inputs["user_context"]
        channel_id = inputs["channel_id"]
        history = client.conversations_history(channel=channel_id, limit=10)["messages"]
        conversation = parse_conversation(history)

        summary = get_provider_response(user_context["id"], SUMMARIZE_CHANNEL_WORKFLOW, conversation)

        complete({"user_context": user_context, "response": summary})
    except Exception as e:
        logger.exception(e)
        fail(e)
```

### Asking Bolty a question {#ask-app}

To ask Bolty a question, you can chat with Bolty in any channel the app is in. Use the `\ask-bolty` slash command to provide a prompt for Bolty to answer. Note that Bolty is currently not supported in threads.

You can also navigate to **Bolty** in your **Apps** list and select the **Messages** tab to chat with Bolty directly.

![Ask Bolty](8.png)

## Next steps {#next-steps}

Congratulations! You've successfully integrated the power of AI into your workspace. Check out these links to take the next steps in your Bolt for Python journey.

- To learn more about Bolt for Python, refer to the [Getting started](/tools/bolt-python/getting-started) documentation.
- For more details about creating workflow steps using the Bolt SDK, refer to the [workflow steps for Bolt](/workflows/workflow-steps) guide.