# Authorization

Authorization is the process of determining which Slack credentials should be available while processing an incoming Slack request.

Apps installed on a single workspace can pass their bot token into the `App` constructor using the `token` parameter. However, if your app will be installed on multiple workspaces, you have two options:

* Use the built-in OAuth support. This will handle setting up OAuth routes and verifying state. See [authenticating with OAuth](/tools/bolt-python/concepts/authenticating-oauth) for more details.
* Set the `authorize` parameter to a function upon `App` instantiation. The `authorize` function should return [an instance of `AuthorizeResult`](https://github.com/slackapi/bolt-python/blob/main/slack_bolt/authorization/authorize_result.py), which contains information about who and where the request is coming from.

`AuthorizeResult` should have a few specific properties, all of type `str`:
- Either **`bot_token`** (xoxb) *or* **`user_token`** (xoxp) are **required**. Most apps will use `bot_token` by default. Passing a token allows built-in functions (like `say()`) to work.
- **`bot_user_id`** and **`bot_id`**, if using a `bot_token`.
- **`enterprise_id`** and **`team_id`**, which can be found in requests sent to your app.
- **`user_id`** only when using `user_token`.

## Example

```python
import os
from slack_bolt import App
# Import the AuthorizeResult class
from slack_bolt.authorization import AuthorizeResult

# This is just an example (assumes there are no user tokens)
# You should store authorizations in a secure DB
installations = [
    {
      "enterprise_id": "E1234A12AB",
      "team_id": "T12345",
      "bot_token": "xoxb-123abc",
      "bot_id": "B1251",
      "bot_user_id": "U12385"
    },
    {
      "team_id": "T77712",
      "bot_token": "xoxb-102anc",
      "bot_id": "B5910",
      "bot_user_id": "U1239",
      "enterprise_id": "E1234A12AB"
    }
]

def authorize(enterprise_id, team_id, logger):
    # You can implement your own logic to fetch token here
    for team in installations:
        # enterprise_id doesn't exist for some teams
        is_valid_enterprise = "enterprise_id" not in team or enterprise_id == team["enterprise_id"]
        if is_valid_enterprise and team["team_id"] == team_id:
          # Return an instance of AuthorizeResult
          # If you don't store bot_id and bot_user_id, could also call `from_auth_test_response` with your bot_token to automatically fetch them
          return AuthorizeResult(
              enterprise_id=enterprise_id,
              team_id=team_id,
              bot_token=team["bot_token"],
              bot_id=team["bot_id"],
              bot_user_id=team["bot_user_id"]
          )

    logger.error("No authorization information was found")

app = App(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    authorize=authorize
)
```

## Handling failed token lookups {#handling-failed-token-lookups}

In the event that you receive events from disconnected teams, make sure to gracefully drop these unauthorized payloads by returning `None` to silently drop the payload as follows.

In the custom `authorize` callback, if a token lookup fails due to an `unknown team_id`, you should return `None` rather than raising an exception (such as `BoltUnauthorizedError`). Bolt's authorization middleware will recognize the `None` response as an authorization failure and immediately halt execution, silently dropping the payload without generating server error logs.

Additionally, the `user_facing_authorize_error_message` parameter strictly controls the ephemeral message sent back to the end user via the Slack UI. It does not suppress internal server logs or exceptions. To achieve both the desired UI behavior and clean server logs, pair this parameter with returning `None` in your authorize function.
