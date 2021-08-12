# AWS Lambda Bolt Python Examples

This directory contains two example apps. Both respond to the Slash Command
`/hello-bolt-python-lambda` and both respond to app at-mentions.

The "Lazy Lambda Listener" example is the simpler application and it leverages
AWS Lambda and AWS API Gateway to execute the Bolt app logic in Lambda and
expose the application HTTP routes to the internet via API Gateway. The "OAuth
Lambda Listener" example additionally includes OAuth flow handling routes and uses
AWS S3 to store workspace installation credentials and OAuth flow state
variables, enabling your app to be installed by anyone.

Instructions on how to set up and deploy each example are provided below.

## Lazy Lambda Listener Example Bolt App

1. You need an AWS account and your AWS credentials set up on your machine.
2. Make sure you have an AWS IAM Role defined with the needed permissions for
   your Lambda function powering your Slack app:
  - Head to the AWS IAM section of AWS Console
  - Click Roles from the menu
  - Click the Create Role button
  - Under "Select type of trusted entity", choose "AWS service"
  - Under "Choose a use case", select "Common use cases: Lambda"
  - Click "Next: Permissions"
  - Under "Attach permission policies", enter "lambda" in the Filter input
  - Check the "AWSLambdaBasicExecutionRole" and "AWSLambdaExecute" policies
  - Click "Next: tags"
  - Click "Next: review"
  - Enter `bolt_python_lambda_invocation` as the Role name. You can change this
      if you want, but then make sure to update the role name in
      `lazy_aws_lambda_config.yaml`
  - Optionally enter a description for the role, such as "Bolt Python basic
      role"
3. Ensure you have created an app on api.slack.com/apps as per the [Getting
   Started Guide](https://slack.dev/bolt-python/tutorial/getting-started).
   Ensure you have installed it to a workspace.
4. Ensure you have exported your Slack Bot Token and Slack Signing Secret for your
   apps as the environment variables `SLACK_BOT_TOKEN` and
   `SLACK_SIGNING_SECRET`, respectively, as per the [Getting
   Started Guide](https://slack.dev/bolt-python/tutorial/getting-started).
5. You may want to create a dedicated virtual environment for this example app, as
   per the "Setting up your project" section of the [Getting
   Started Guide](https://slack.dev/bolt-python/tutorial/getting-started).
6. Let's deploy the Lambda! Run `./deploy_lazy.sh`. By default it deploys to the
   us-east-1 region in AWS - you can change this at the top of `lazy_aws_lambda_config.yaml` if you wish.
7. Load up AWS Lambda inside the AWS Console - make sure you are in the correct
   region that you deployed your app to. You should see a `bolt_py_function`
   Lambda there.
8. While your Lambda exists, it is not accessible to the internet, so Slack
   cannot send events happening in your Slack workspace to your Lambda. Let's
   fix that by adding an AWS API Gateway in front of your Lambda so that your
   Lambda can accept HTTP requests:
  - Click on your `bolt_py_function` Lambda
  - In the Function Overview, on the left side, click "+ Add Trigger"
  - Select API Gateway from the trigger list
  - Make sure "Create an API" is selected in the dropdown, and choose "HTTP API"
      as the API Type
  - Under Security, select "Open"
  - Click "Add"
9. Congrats! Your Slack app is now accessible to the public. On the left side of
   your `bolt_py_function` Function Overview you should see a purple API Gateway
   icon. Click it.
10. Click Details to expand the details section.
11. Copy the API Endpoint - this is the URL your Lambda function is accessible
    at publicly.
12. We will now inform Slack that this example app can accept Slash Commands.
  - Back on api.slack.com/apps, select your app and choose Slash Commands from the left menu.
  - Click Create New Command
  - By default, the `lazy_aws_lambda.py` function has logic for a
      `/hello-bolt-python-lambda` command. Enter `/hello-bolt-python-lambda` as
      the Command.
  - Under Request URL, paste in the previously-copied API Endpoint from API
      Gateway.
  - Click Save
13. Test it out! Back in your Slack workspace, try typing
    `/hello-bolt-python-lambda hello`.
14. If you have issues, here are some debugging options:
  - Check the Monitor tab under your Lambda. Did the Lambda get invoked? Did it
      respond with an error? Investigate the graphs to see how your Lambda is
      behaving.
  - From this same Monitor tab, you can also click "View Logs in CloudWatch" to
      see the execution logs for your Lambda. This can be helpful to see what
      errors are being raised.

## OAuth Lambda Listener Example Bolt App

1. You need an AWS account and your AWS credentials set up on your machine.
2. Make sure you have an AWS IAM Role defined with the needed permissions for
   your Lambda function powering your Slack app:
  - Head to the AWS IAM section of AWS Console
  - Click Roles from the menu
  - Click the Create Role button
  - Under "Select type of trusted entity", choose "AWS service"
  - Under "Choose a use case", select "Common use cases: Lambda"
  - Click "Next: Permissions"
  - Under "Attach permission policies", enter "lambda" in the Filter input
  - Check the "AWSLambdaBasicExecutionRole" and "AWSLambdaExecute" policies
  - Under "Attach permission policies", enter "s3" in the Filter input
  - Check the "AWSS3FullAccess" policy
  - Click "Next: tags"
  - Click "Next: review"
  - Enter `bolt_python_s3_storage` as the Role name. You can change this
      if you want, but then make sure to update the role name in
      `aws_lambda_oauth_config.yaml`
  - Optionally enter a description for the role, such as "Bolt Python with S3
      access role"
3. Ensure you have created an app on api.slack.com/apps as per the [Getting
   Started Guide](https://slack.dev/bolt-python/tutorial/getting-started).
   You do not need to ensure you have installed it to a workspace, as the OAuth
   flow will provide your app the ability to be installed by anyone.
4. You will need to create two S3 buckets: one to store installation credentials
   (when a new Slack workspace installs your app) and one to store state
   variables during the OAuth flow. You will need the names of these buckets in
   the next step.
5. You need many environment variables exported! Specifically the following from
   api.slack.com/apps:
  - `SLACK_SIGNING_SECRET`: Signing Secret from Basic Information page
  - `SLACK_CLIENT_ID`: Client ID from Basic Information page
  - `SLACK_CLIENT_SECRET`: Client Secret from Basic Information page
  - `SLACK_SCOPES="app_mentions:read,chat:write"`: Which scopes this application
      needs
  - `SLACK_INSTALLATION_S3_BUCKET_NAME`: The name of one of the S3 buckets you
      created
  - `SLACK_STATE_S3_BUCKET_NAME`: The name of the other S3 bucket you created
  - `SLACK_LAMBDA_PATH`: ??? TODO
6. Let's deploy the Lambda! Run `./deploy_oauth.sh`. By default it deploys to the
   us-east-1 region in AWS - you can change this at the top of `aws_lambda_oauth_config.yaml` if you wish.
7. Load up AWS Lambda inside the AWS Console - make sure you are in the correct
   region that you deployed your app to. You should see a `bolt_py_oauth_function`
   Lambda there.
8. While your Lambda exists, it is not accessible to the internet, so Slack
   cannot send events happening in your Slack workspace to your Lambda. Let's
   fix that by adding an AWS API Gateway in front of your Lambda so that your
   Lambda can accept HTTP requests:
  - Click on your `bolt_py_oauth_function` Lambda
  - In the Function Overview, on the left side, click "+ Add Trigger"
  - Select API Gateway from the trigger list
  - Make sure "Create an API" is selected in the dropdown, and choose "HTTP API"
      as the API Type
  - Under Security, select "Open"
  - Click "Add"
9. Congrats! Your Slack app is now accessible to the public. On the left side of
   your `bolt_py_oauth_function` Function Overview you should see a purple API Gateway
   icon. Click it.
10. Click Details to expand the details section.
11. Copy the API Endpoint - this is the URL your Lambda function is accessible
    at publicly.
12. We will now inform Slack that this example app can accept Slash Commands.
  - Back on api.slack.com/apps, select your app and choose Slash Commands from the left menu.
  - Click Create New Command
  - By default, the `aws_lambda_oauth.py` function has logic for a
      `/hello-bolt-python-lambda` command. Enter `/hello-bolt-python-lambda` as
      the Command.
  - Under Request URL, paste in the previously-copied API Endpoint from API
      Gateway.
  - Click Save
13. We also need to register the API Endpoint as the OAuth redirect URL:
  - Load up the "OAuth &amp; Permissions" page on api.slack.com/apps
  - Scroll down to Redirect URLs
  - Copy the API endpoint in - but remove the path portion. The Redirect URL
      needs to only _partially_ match where we will send users.
14. You can now install the app to any workspace!
15. Test it out! Once installed to a Slack workspace, try typing
    `/hello-bolt-python-lambda hello`.
16. If you have issues, here are some debugging options:
  - Check the Monitor tab under your Lambda. Did the Lambda get invoked? Did it
      respond with an error? Investigate the graphs to see how your Lambda is
      behaving.
  - From this same Monitor tab, you can also click "View Logs in CloudWatch" to
      see the execution logs for your Lambda. This can be helpful to see what
      errors are being raised.
