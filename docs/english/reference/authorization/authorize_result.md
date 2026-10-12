---
sidebar_label: authorize_result
title: slack_bolt.authorization.authorize_result
---

## `AuthorizeResult`

```python
AuthorizeResult(*, enterprise_id, team_id, team=None, url=None, bot_user_id=None, bot_id=None, bot_token=None, bot_scopes=None, user_id=None, user=None, user_token=None, user_scopes=None)
```

Bases: dict

Authorize function call result.

Initialize the authorize function call result.

**Parameters:**

- **enterprise_id** (Optional[str]) – Organization ID (Enterprise Grid) starting with `E`
- **team_id** (Optional[str]) – Workspace ID starting with `T`
- **team** (Optional[str]) – Workspace name
- **url** (Optional[str]) – Workspace slack.com URL
- **bot_user_id** (Optional[str]) – Bot user's User ID starting with either `U` or `W`
- **bot_id** (Optional[str]) – Bot ID starting with `B`
- **bot_token** (Optional[str]) – Bot user access token starting with `xoxb-`
- **bot_scopes** (Optional[Union[Sequence[str], str]]) – The scopes associated with the bot token
- **user_id** (Optional[str]) – The request user ID
- **user** (Optional[str]) – The request user's name
- **user_token** (Optional[str]) – User access token starting with `xoxp-`
- **user_scopes** (Optional[Union[Sequence[str], str]]) – The scopes associated with the user token
