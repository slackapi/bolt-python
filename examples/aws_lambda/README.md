# Lazy Lambda Listener Example Bolt App

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
7. Load up AWS Lambda inside the AWS Console - make sure you are in the  correct
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
