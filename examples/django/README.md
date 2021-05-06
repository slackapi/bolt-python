Follow the instructions [here](https://slack.dev/bolt-python/concepts#authenticating-oauth) for configuring OAuth flow supported Slack apps. This example works with the default env variables such as `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, `SLACK_SCOPES`, `SLACK_SIGNING_SECRET`, and so forth.

```
pip install -r requirements.txt
export SLACK_CLIENT_ID=
export SLACK_CLIENT_SECRET=
export SLACK_SCOPES=commands.chat:write
export SLACK_SIGNING_SECRET=

python manage.py migrate
python manage.py runserver 0.0.0.0:3000
```