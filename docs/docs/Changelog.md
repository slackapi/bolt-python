<a name="v1.19.1"></a>
# [version 1.19.1 (v1.19.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.19.1) - 03 Jul 2024

### Changes

* [#1104](https://github.com/slackapi/bolt-python/issues/1104) Add bot|user_scopes to context.authorize_result set by SingleTeamAuthorization - Thanks [@seratch](https://github.com/seratch) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/84?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.19.0...v1.19.1

[Changes][v1.19.1]


<a name="v1.19.0"></a>
# [v1.19.0](https://github.com/slackapi/bolt-python/releases/tag/v1.19.0) - 10 Jun 2024

## New Features

## WSGI Adapter

https://github.com/slackapi/bolt-python/pull/1085 by [@WilliamBergamin](https://github.com/WilliamBergamin) introduces an WSGI adapter, this allows bolt to be deployed in production without the need of a 3rd party WSGI compatible web framework. check out the examples in [examples/wsgi](https://github.com/slackapi/bolt-python/tree/main/examples/wsgi)

## Deprecate Steps From Apps
https://github.com/slackapi/bolt-python/pull/1089 by [@WilliamBergamin](https://github.com/WilliamBergamin) adds deprecation warnings to Steps from Apps components and documentation. 

## What's Changed
### Fixes
* Fix typo in ja_listening_events.md by [@johtani](https://github.com/johtani) in https://github.com/slackapi/bolt-python/pull/1022
* Fix [#1074](https://github.com/slackapi/bolt-python/issues/1074) Customize user-facing message sent when an installation is not managed by bolt-python app by [@seratch](https://github.com/seratch) in https://github.com/slackapi/bolt-python/pull/1077

### Tests
* Improve socket mode tests by [@WilliamBergamin](https://github.com/WilliamBergamin) in https://github.com/slackapi/bolt-python/pull/991
* remove unused multiprocessing test mode by [@WilliamBergamin](https://github.com/WilliamBergamin) in https://github.com/slackapi/bolt-python/pull/1011
* Replace Flask-Sockets with aiohttp for testing  by [@WilliamBergamin](https://github.com/WilliamBergamin) in https://github.com/slackapi/bolt-python/pull/1012
* feat: improve test speed by [@WilliamBergamin](https://github.com/WilliamBergamin) in https://github.com/slackapi/bolt-python/pull/1017
### Dependabot
* Bump actions/checkout from 3 to 4 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1038
* Bump actions/setup-python from 4 to 5 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1040
* Bump actions/stale from 4.0.0 to 9.0.0 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1042
* Update werkzeug requirement from \<3,\>=2 to \>=2,\<4 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1041
* Update pytest requirement from \<7,\>=6.2.5 to \>=6.2.5,\<9 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1043
* Update flask requirement from \<3,\>=1 to \>=1,\<4 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1044
* Update gunicorn requirement from \<21,\>=20 to \>=20,\<22 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1045
* Update moto requirement from \<5,\>=3 to \>=3,\<6 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1046
* Bump codecov/codecov-action from 3 to 4 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1039
* Update django requirement from \<5,\>=3 to \>=3,\<6 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1051
* Update docker requirement from \<6,\>=5 to \>=5,\<8 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1052
* Update websockets requirement from \<11 to \<13 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1054
* Update sanic requirement from \<23,\>=22 to \>=22,\<24 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1055
* Update click requirement from \<=8.0.4 to \<=8.1.7 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1057
* Update pytest-cov requirement from \<5,\>=3 to \>=3,\<6 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1067
* Update gunicorn requirement from \<22,\>=20 to \>=20,\<23 by [@dependabot](https://github.com/dependabot) in https://github.com/slackapi/bolt-python/pull/1073

### Misc
* Configuring with pyproject.toml by [@WilliamBergamin](https://github.com/WilliamBergamin) in https://github.com/slackapi/bolt-python/pull/996
* Maintain metadata by [@WilliamBergamin](https://github.com/WilliamBergamin) in https://github.com/slackapi/bolt-python/pull/999
* feat: use dependabot to maintain packages by [@WilliamBergamin](https://github.com/WilliamBergamin) in https://github.com/slackapi/bolt-python/pull/1037
* release: version 1.19.0 by [@WilliamBergamin](https://github.com/WilliamBergamin) in https://github.com/slackapi/bolt-python/pull/1091


## New Contributors
* [@johtani](https://github.com/johtani) made their first contribution in https://github.com/slackapi/bolt-python/pull/1022
* [@dependabot](https://github.com/dependabot) made their first contribution in https://github.com/slackapi/bolt-python/pull/1038

**Full Changelog**: https://github.com/slackapi/bolt-python/compare/v1.18.1...v1.19.0

[Changes][v1.19.0]


<a name="v1.19.0rc1"></a>
# [version 1.19.0 RC1 (v1.19.0rc1)](https://github.com/slackapi/bolt-python/releases/tag/v1.19.0rc1) - 25 Jan 2024

Check https://github.com/slackapi/bolt-python/releases/tag/v1.19.0rc1 instead

[Changes][v1.19.0rc1]


<a name="v1.18.1"></a>
# [version 1.18.1 (v1.18.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.18.1) - 21 Nov 2023

### Changes

* [#895](https://github.com/slackapi/bolt-python/issues/895) Add metadata to respond method - Thanks [@seratch](https://github.com/seratch) 
* [#917](https://github.com/slackapi/bolt-python/issues/917) Add port parameter to web_app - Thanks [@butsyk](https://github.com/butsyk) 
* [#990](https://github.com/slackapi/bolt-python/issues/990) Fix [#988](https://github.com/slackapi/bolt-python/issues/988) app.action listener should accept block_id-only constraints for bolt-js feature parity - Thanks [@seratch](https://github.com/seratch) [@darkfoxprime](https://github.com/darkfoxprime)

Test code improvements:
* [#918](https://github.com/slackapi/bolt-python/issues/918) Fix [#892](https://github.com/slackapi/bolt-python/issues/892) Codecov CI job for this project hangs - Thanks [@vgnshiyer](https://github.com/vgnshiyer) 
* [#987](https://github.com/slackapi/bolt-python/issues/987) Fix SocketMode Test - Thanks [@WilliamBergamin](https://github.com/WilliamBergamin) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/79?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.18.0...v1.18.1

[Changes][v1.18.1]


<a name="v1.18.0"></a>
# [version 1.18.0 (v1.18.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.18.0) - 26 Apr 2023

### Changes

* [#891](https://github.com/slackapi/bolt-python/issues/891) Add url, team, user to AuthorizeResult properties (as optional ones) - Thanks [@seratch](https://github.com/seratch) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/77?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.17.2...v1.18.0

[Changes][v1.18.0]


<a name="v1.17.2"></a>
# [version 1.17.2 (v1.17.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.17.2) - 18 Apr 2023

### Changes

* [#885](https://github.com/slackapi/bolt-python/issues/885) Improve the default handler when raise_error_for_unhandled_request is true - Thanks [@seratch](https://github.com/seratch)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/78?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.17.1...v1.17.2

[Changes][v1.17.2]


<a name="v1.17.1"></a>
# [version 1.17.1 (v1.17.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.17.1) - 13 Apr 2023

### Changes

* [#882](https://github.com/slackapi/bolt-python/issues/882) Improve the default OAuth page renderers not to embed any params without escaping them - Thanks [@seratch](https://github.com/seratch) 
* Upgrade the slack-sdk package version to the latest - Thanks [@seratch](https://github.com/seratch) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/76?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.17.0...v1.17.1

[Changes][v1.17.1]


<a name="v1.17.0"></a>
# [version 1.17.0 (v1.17.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.17.0) - 27 Mar 2023

### New Features

#### Updates on `AuthorizeResult` properties

In v1.17, two new optional properties `bot_scopes` and `user_scopes` have been added to the `AuthorizeResult` / `AsyncAuthorizeResult` classes. These properties are used to associate specific scopes with `bot_token` and `user_token`, and the built-in InstallationStore automatically resolves them.

* `bot_scopes`: the scopes associated with the `bot_token`; this can be absent when `bot_token` does not exist
* `user_scopes`: the scopes associated with the `user_token`; this can be absent when `user_token` does not exist

These properties are optional, so all the existing `Authorize` / `AsyncAuthorize` sub classes are expected to continue functioning without any code changes.

Also, this version includes the fix for the existing bug where the `user_id` can be absent when both `bot_token` and `user_token` exist.

Please refer to https://github.com/slackapi/bolt-python/pull/855 or the details of the changes.

#### New actor IDs in `context`

Starting in v1.17, `context` objects in middleware and listeners provide a few new properties -- `actor_enterprise_id`, `actor_team_id`, and `actor_user_id`--, in addition to existing `enterprise_id`, `team_id`, and `user_id`. You should be curious about the difference. The new "actor" IDs remain the same for interactivity events such as slash commands, global shortcuts, etc. The key difference can appear when your app handles Events API subscription requests such as "app_mention" and "message" events in Slack Connect channels and/or when your app is distributed, and it has multiple workspace installations.

When your app is installed into multiple workspaces and/or by multiple users, the `context.user_id` can be any of the installed users' ones. Also, if your app is installed into multiple workspaces plus your app is added to a Slack Connect channel shared by those organizations, `context.enterprise_id`, `context.team_id`, and `context.user_id` are associated with any of the workspaces/organizations. Therefore, the tokens provided by bolt-python are still correct, as the tokens are associated with any installations for the received event.

However, when a user mentions your app's bot user in the Slack Connect channel, your app may desire to quickly check if the user (let us call this user "actor") has granted the app with the user's scopes. In this scenario, `context.user_id` etc. does not work. Instead, you must write your code to identify the "actor"'s workspace and user ID. The newly added "actor" IDs can easily help you handle such patterns. You can rely on the "actor" IDs as long as they exist. In other words, note that they can be absent for some events due to the lack of response data from the Slack server side. Such patterns can be improved by either SDK updates or server-side changes in future versions.

#### New `user_token_resolution` option

Related to the above, we added a new option called `user_token_resolution: str` for `App` / `AsyncApp` initialization. The available values for the option are `"authed_user"` and `"actor"`. The default value is `"authed_user"`, which is fully backward-compatible.

When you set `"actor"` for the option, your OAuth-enabled app's authorize function can behave differently. More specifically, the `authorize` function receives all the "actor" IDs. The built-in `InstallationStore`-based authorize tries to resolve the user token per request using "actor" IDs instead of `context.user_id`.

Setting `"actor"` for this option can be beneficial for the apps that require all the users to grant the app some use scopes. In this scenario, your app can easily identify the users who haven't installed the app with sufficient user scopes just by checking the existence of the user token and user scopes in the `context.authorize_result` object.

If your app does not request any user scopes when installing the app into a workspace, configuring this option does not have any effect on your app.

#### New `before_authorize` option

To skip unnecessary workload in a bolt-python app, now you can use `before_authorize` middleware function for it. Let's say your app receives "message" events but there is nothing to do with subtyped ones such as "message_changed" and "message_deleted". Your `authorize` function looks up installation data in your database and performs `auth.test` API calls. In this case, `before_authorize` can enable the app to skip the `authorize` operations for subtyped message events this way:

```python
def skip_message_changed_events(payload: dict, next_):
    if payload.get("type") == "message" and payload.get("subtype") in ["message_changed", "message_deleted"]:
        # acknowledge the request and skip all the following middleware/listeners
        return BoltResponse(status=200, body="")
    next_()
```

### Changes

* [#855](https://github.com/slackapi/bolt-python/issues/855) [#858](https://github.com/slackapi/bolt-python/issues/858) Enhance AuthorizeResult to have bot/user_scopes & resolve user_id for user token - Thanks [@seratch](https://github.com/seratch)
* [#854](https://github.com/slackapi/bolt-python/issues/854) Introduce actor enterprise/team/user_id for Slack Connect events  - Thanks [@seratch](https://github.com/seratch)
* [#869](https://github.com/slackapi/bolt-python/issues/869) Add before_authorize middleware - Thanks [@seratch](https://github.com/seratch)
* [#856](https://github.com/slackapi/bolt-python/issues/856) Update optional chalice dependency version range - Thanks [@seratch](https://github.com/seratch)
* [#861](https://github.com/slackapi/bolt-python/issues/861) Improve token rotation error handling and installation error text - Thanks [@seratch](https://github.com/seratch) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/66?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.16.4...v1.17.0

[Changes][v1.17.0]


<a name="v1.17.0rc4"></a>
# [version 1.17.0 RC4 (v1.17.0rc4)](https://github.com/slackapi/bolt-python/releases/tag/v1.17.0rc4) - 21 Mar 2023

Check https://github.com/slackapi/bolt-python/releases/tag/v1.17.0 instead

[Changes][v1.17.0rc4]


<a name="v1.17.0rc3"></a>
# [version 1.17.0 RC3 (v1.17.0rc3)](https://github.com/slackapi/bolt-python/releases/tag/v1.17.0rc3) - 15 Mar 2023

Check https://github.com/slackapi/bolt-python/releases/tag/v1.17.0rc4 instead

[Changes][v1.17.0rc3]


<a name="v1.17.0rc2"></a>
# [version 1.17.0 RC2 (v1.17.0rc2)](https://github.com/slackapi/bolt-python/releases/tag/v1.17.0rc2) - 13 Mar 2023

Check https://github.com/slackapi/bolt-python/releases/tag/v1.17.0rc3 instead

[Changes][v1.17.0rc2]


<a name="v1.17.0rc1"></a>
# [version 1.17.0 RC1 (v1.17.0rc1)](https://github.com/slackapi/bolt-python/releases/tag/v1.17.0rc1) - 13 Mar 2023

Check https://github.com/slackapi/bolt-python/releases/tag/v1.17.0rc2 instead

[Changes][v1.17.0rc1]


<a name="v1.16.4"></a>
# [version 1.16.4 (v1.16.4)](https://github.com/slackapi/bolt-python/releases/tag/v1.16.4) - 10 Mar 2023

### Changes

* [#853](https://github.com/slackapi/bolt-python/issues/853) Add team param support to the /slack/install endpoint - Thanks [@seratch](https://github.com/seratch) 
* [#851](https://github.com/slackapi/bolt-python/issues/851) Enable developers to pass fully implemented authorize along with installation_store - Thanks [@seratch](https://github.com/seratch) 
* [#848](https://github.com/slackapi/bolt-python/issues/848) Enable developers to define app.message listener without args to capture all messages - Thanks [@seratch](https://github.com/seratch) 
* [#852](https://github.com/slackapi/bolt-python/issues/852) Fix [#850](https://github.com/slackapi/bolt-python/issues/850) by upgrading slack-sdk version to the latest - Thanks [@seratch](https://github.com/seratch) [@garymalaysia](https://github.com/garymalaysia)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/75?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.16.3...v1.16.4

[Changes][v1.16.4]


<a name="v1.16.3"></a>
# [version 1.16.3 (v1.16.3)](https://github.com/slackapi/bolt-python/releases/tag/v1.16.3) - 08 Mar 2023

### Changes

* [#844](https://github.com/slackapi/bolt-python/issues/844) Fix [#842](https://github.com/slackapi/bolt-python/issues/842) Cannot pass thread_ts to respond() utilit - Thanks [@athlindemark](https://github.com/athlindemark) [@seratch](https://github.com/seratch) 

#### Document Changes

* [#835](https://github.com/slackapi/bolt-python/issues/835) Add documention for injected 'args' param option - Thanks [@YSaxon](https://github.com/YSaxon)
* [#831](https://github.com/slackapi/bolt-python/issues/831) Added redirect url to readme - Thanks [@Smyja](https://github.com/Smyja)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/74?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.16.2...v1.16.3

[Changes][v1.16.3]


<a name="v1.16.2"></a>
# [version 1.16.2 (v1.16.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.16.2) - 15 Feb 2023

### Changes

* [#825](https://github.com/slackapi/bolt-python/issues/825) Fix perform_bot_token_rotation call in AsyncInstallationStoreAuthorize - Thanks [@ccaruceru](https://github.com/ccaruceru)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/73?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.16.1...v1.16.2

[Changes][v1.16.2]


<a name="v1.16.1"></a>
# [version 1.16.1 (v1.16.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.16.1) - 19 Dec 2022

### Changes

* [#794](https://github.com/slackapi/bolt-python/issues/794) Fix [#793](https://github.com/slackapi/bolt-python/issues/793) by adding pyramid_request property to Bolt context - Thanks [@dz0ny](https://github.com/dz0ny) [@seratch](https://github.com/seratch) 

#### Document / Project Updates

* [#792](https://github.com/slackapi/bolt-python/issues/792) Adding Handling views on close documentation - Thanks [@BrandonDalton](https://github.com/BrandonDalton) 
* [#762](https://github.com/slackapi/bolt-python/issues/762) Add documentation related to how to handle view_closed events - Thanks [@filmaj](https://github.com/filmaj) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/72?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.16.0...v1.16.1

[Changes][v1.16.1]


<a name="v1.16.0"></a>
# [version 1.16.0 (v1.16.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.16.0) - 08 Dec 2022

### New Features

#### ASGI Adapter

Since this version, a new adapter that implements the [ASGI standard](https://asgi.readthedocs.io/en/latest/) is available. The novel adapter brings the following benefits to developers:

* A builtin way to deploy HTTP apps to production using the ASGI standard
* Allow bolt to be deployed on a web servers such as [daphne](https://github.com/django/daphne), [uvicorn](https://www.uvicorn.org/) and [hypercorn](https://pgjones.gitlab.io/hypercorn/index.html) without other dependencies
* A way to create small, lightweight and efficient docker images for bolt python

The adapter is compatible with both `App` and `AsyncApp`. You can run both of the following app code by running `uvicorn app:api --reload --port 3000 --log-level debug`:

```python

from slack_bolt import App
from slack_bolt.adapter.asgi import SlackRequestHandler

app = App()

@app.event("app_mention")
def handle_app_mentions(say):
    say("What's up?")

api = SlackRequestHandler(app)
```

Here is an asyncio-based app:

```python
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.asgi.async_handler import AsyncSlackRequestHandler

app = AsyncApp()

@app.event("app_mention")
async def handle_app_mentions(say):
    await say("What's up?")

api = AsyncSlackRequestHandler(app)
```

To learn more on the implementation and grab more code examples, please check [@WilliamBergamin](https://github.com/WilliamBergamin)'s pull request adding the feature: https://github.com/slackapi/bolt-python/pull/780

### Changes

* [#780](https://github.com/slackapi/bolt-python/issues/780) Add ASGI adapter - Thanks [@WilliamBergamin](https://github.com/WilliamBergamin)

#### Document / Project Updates

* [#779](https://github.com/slackapi/bolt-python/issues/779) Fixing link to message event subtypes docs - Thanks [@filmaj](https://github.com/filmaj) 
* [#776](https://github.com/slackapi/bolt-python/issues/776) CI python 3.6 bug fix - Thanks [@WilliamBergamin](https://github.com/WilliamBergamin) 
* [#770](https://github.com/slackapi/bolt-python/issues/770) Fix [#757](https://github.com/slackapi/bolt-python/issues/757) by using Falcon 3.1.1 - Thanks [@seratch](https://github.com/seratch) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/65?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.15.5...v1.16.0

[Changes][v1.16.0]


<a name="v1.15.5"></a>
# [version 1.15.5 (v1.15.5)](https://github.com/slackapi/bolt-python/releases/tag/v1.15.5) - 17 Nov 2022

### Changes

* [#769](https://github.com/slackapi/bolt-python/issues/769) Fix [#768](https://github.com/slackapi/bolt-python/issues/768) The client arg in a listener does not respect the singleton WebClient's retry_handlers - Thanks [@seratch](https://github.com/seratch)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/70?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.15.4...v1.15.5

[Changes][v1.15.5]


<a name="v1.15.4"></a>
# [version 1.15.4 (v1.15.4)](https://github.com/slackapi/bolt-python/releases/tag/v1.15.4) - 17 Nov 2022

### Changes

* [#766](https://github.com/slackapi/bolt-python/issues/766) Fix [#763](https://github.com/slackapi/bolt-python/issues/763) by improving the suggestion logging for view_closed patterns - Thanks [@seratch](https://github.com/seratch) [@filmaj](https://github.com/filmaj) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/69?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.15.3...v1.15.4

[Changes][v1.15.4]


<a name="v1.15.3"></a>
# [version 1.15.3 (v1.15.3)](https://github.com/slackapi/bolt-python/releases/tag/v1.15.3) - 08 Nov 2022

### Changes

* [#751](https://github.com/slackapi/bolt-python/issues/751) Add Python 3.11 to the supported language versions - Thanks [@seratch](https://github.com/seratch)
* [#758](https://github.com/slackapi/bolt-python/issues/758) Fix [#754](https://github.com/slackapi/bolt-python/issues/754) by adding the async version of Tornado adapter - Thanks [@seratch](https://github.com/seratch) [@castrapel](https://github.com/castrapel)
* [#748](https://github.com/slackapi/bolt-python/issues/748) Fix [#747](https://github.com/slackapi/bolt-python/issues/747) by updating async SQLAlchemy OAuth example code - Thanks [@ntarora](https://github.com/ntarora)
* [#752](https://github.com/slackapi/bolt-python/issues/752) Update code_cov upload method - Thanks [@WilliamBergamin](https://github.com/WilliamBergamin)
* [#745](https://github.com/slackapi/bolt-python/issues/745) Remove 2020-resolver - Thanks [@WilliamBergamin](https://github.com/WilliamBergamin)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/68?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.15.2...v1.15.3

[Changes][v1.15.3]


<a name="v1.15.2"></a>
# [version 1.15.2 (v1.15.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.15.2) - 18 Oct 2022

### Changes

* [#741](https://github.com/slackapi/bolt-python/issues/741) Fix [#738](https://github.com/slackapi/bolt-python/issues/738) Add more keyword args to say utility - Thanks [@seratch](https://github.com/seratch) [@jacklowrie](https://github.com/jacklowrie)
* [#736](https://github.com/slackapi/bolt-python/issues/736) Add context 'user_id' extraction for 'message_changed' and 'message_deleted' events - Thanks [@eddyg](https://github.com/eddyg) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/67?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.15.1...v1.15.2

[Changes][v1.15.2]


<a name="v1.15.1"></a>
# [version 1.15.1 (v1.15.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.15.1) - 06 Oct 2022

### Changes

* [#734](https://github.com/slackapi/bolt-python/issues/734) Fix context.team_id for view interactions in a Slack Connect channel - Thanks [@seratch](https://github.com/seratch) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/64?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.15.0...v1.15.1

[Changes][v1.15.1]


<a name="v1.15.0"></a>
# [version 1.15.0 (v1.15.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.15.0) - 30 Sep 2022

### Changes

* [#722](https://github.com/slackapi/bolt-python/issues/722) Fix [#721](https://github.com/slackapi/bolt-python/issues/721) Passing a global dict object without channel prop can cause issues among requests - Thanks [@seratch](https://github.com/seratch) [@gk-patel](https://github.com/gk-patel)
* [#714](https://github.com/slackapi/bolt-python/issues/714) Change to create a WebClient per request for safety - Thanks [@seratch](https://github.com/seratch) 
* [#726](https://github.com/slackapi/bolt-python/issues/726) [#727](https://github.com/slackapi/bolt-python/issues/727) Bump Sanic, websockets packages to the latest major versions - Thanks [@e-zim](https://github.com/e-zim) [@JWZepf](https://github.com/JWZepf)

#### Document Changes

* [#725](https://github.com/slackapi/bolt-python/issues/725) Development release steps in guide - Thanks [@WilliamBergamin](https://github.com/WilliamBergamin) 
* [#690](https://github.com/slackapi/bolt-python/issues/690) Issue [#660](https://github.com/slackapi/bolt-python/issues/660): Replace HTML entities before markdownify in docs - Thanks [@acq688](https://github.com/acq688)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/60?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.14.3...v1.15.0

[Changes][v1.15.0]


<a name="v1.14.3"></a>
# [version 1.14.3 (v1.14.3)](https://github.com/slackapi/bolt-python/releases/tag/v1.14.3) - 26 Jul 2022

### Changes

* [#689](https://github.com/slackapi/bolt-python/issues/689) Fix [#688](https://github.com/slackapi/bolt-python/issues/688) kwarg injection does not work with decorated functions - Thanks [@seratch](https://github.com/seratch) [@deppe](https://github.com/deppe)

#### Document Changes

* [#686](https://github.com/slackapi/bolt-python/issues/686) Add anchors and add contribute link to sidebar - Thanks [@wongjas](https://github.com/wongjas) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/63?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.14.2...v1.14.3

[Changes][v1.14.3]


<a name="v1.14.2"></a>
# [version 1.14.2 (v1.14.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.14.2) - 21 Jul 2022

### Changes

* [#684](https://github.com/slackapi/bolt-python/issues/684) Fix [#683](https://github.com/slackapi/bolt-python/issues/683) IgnoringSelfEvents middleware does not filter out Message sent via response_url - Thanks [@seratch](https://github.com/seratch) [@deppe](https://github.com/deppe)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/62?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.14.1...v1.14.2

[Changes][v1.14.2]


<a name="v1.14.1"></a>
# [version 1.14.1 (v1.14.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.14.1) - 12 Jul 2022

### Changes

* [#679](https://github.com/slackapi/bolt-python/issues/679) Allow lazy function invocation to target version/alias - Thanks [@angrychimp](https://github.com/angrychimp) 
* [#662](https://github.com/slackapi/bolt-python/issues/662) Make the flake8 and black settings consistent - Thanks [@seratch](https://github.com/seratch) 

#### Document / Example Updates

* [#665](https://github.com/slackapi/bolt-python/issues/665) Fix [#664](https://github.com/slackapi/bolt-python/issues/664) Django example installation store improvement - Thanks [@seratch](https://github.com/seratch) [@DataGreed](https://github.com/DataGreed)
* [#659](https://github.com/slackapi/bolt-python/issues/659) [#661](https://github.com/slackapi/bolt-python/issues/661) Change AWS API Gateway to Lambda Function URL in documents - Thanks [@Globart1337](https://github.com/Globart1337)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/61?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.14.0...v1.14.1

[Changes][v1.14.1]


<a name="v1.14.0"></a>
# [version 1.14.0 (v1.14.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.14.0) - 18 May 2022

### Changes

* [#649](https://github.com/slackapi/bolt-python/issues/649) Add Google Cloud Functions adapter (ref [#646](https://github.com/slackapi/bolt-python/issues/646)) - Thanks [@seratch](https://github.com/seratch) 
* [#647](https://github.com/slackapi/bolt-python/issues/647) Remove noqa comments and add `__all__` to `__init__.py` files - Thanks [@seratch](https://github.com/seratch) 

#### Document Updates

* [#648](https://github.com/slackapi/bolt-python/issues/648) Clarify "Setting up events" section - Thanks [@hestonhoffman](https://github.com/hestonhoffman) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/56?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.13.2...v1.14.0

[Changes][v1.14.0]


<a name="v1.13.2"></a>
# [version 1.13.2 (v1.13.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.13.2) - 11 May 2022

### Changes

* [#645](https://github.com/slackapi/bolt-python/issues/645) Fix [#644](https://github.com/slackapi/bolt-python/issues/644) app.message listener does not handle events when a file is attached - Thanks [@seratch](https://github.com/seratch) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/58?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.13.1...v1.13.2

[Changes][v1.13.2]


<a name="v1.13.1"></a>
# [version 1.13.1 (v1.13.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.13.1) - 29 Apr 2022

### Changes

* [#640](https://github.com/slackapi/bolt-python/issues/640) Fix [#639](https://github.com/slackapi/bolt-python/issues/639) is_enterprise_install does not exist in context object - Thanks [@seratch](https://github.com/seratch) [@Sadisms](https://github.com/Sadisms) 
* [#636](https://github.com/slackapi/bolt-python/issues/636) Upgrade pytype version to the latest - Thanks [@seratch](https://github.com/seratch) 
* [#638](https://github.com/slackapi/bolt-python/issues/638) Enable Flake8 in the CI builds - Thanks [@seratch](https://github.com/seratch) 

#### Document Updates

* [#621](https://github.com/slackapi/bolt-python/issues/621) Improve the OAuth Lambda deployment instructs - Thanks [@srajiang](https://github.com/srajiang) 
* [#623](https://github.com/slackapi/bolt-python/issues/623) Add Socket Mode healthcheck endpoint examples ([#622](https://github.com/slackapi/bolt-python/issues/622)) - Thanks [@ImRohan01](https://github.com/ImRohan01) [@seratch](https://github.com/seratch) 
* [#633](https://github.com/slackapi/bolt-python/issues/633) Update AWS example documentation with correct AWS Lambda roles required - Thanks [@cp2423](https://github.com/cp2423) [@filmaj](https://github.com/filmaj) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/57?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.13.0...v1.13.1

[Changes][v1.13.1]


<a name="v1.13.0"></a>
# [version 1.13.0 (v1.13.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.13.0) - 18 Mar 2022

### Changes

* [#618](https://github.com/slackapi/bolt-python/issues/618) Fix [#617](https://github.com/slackapi/bolt-python/issues/617) Respect the configuration of logger parameter across App/AsyncApp loggers - Thanks [@seratch](https://github.com/seratch) [@brian-nguyen-bolt](https://github.com/brian-nguyen-bolt)  
* [#616](https://github.com/slackapi/bolt-python/issues/616) Fix type hint for event constraint to allow None subtypes - Thanks [@alexrashed](https://github.com/alexrashed)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/55?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.12.0...v1.13.0

[Changes][v1.13.0]


<a name="v1.12.0"></a>
# [version 1.12.0 (v1.12.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.12.0) - 17 Mar 2022

### Changes

* [#614](https://github.com/slackapi/bolt-python/issues/614) Add Falcon (ASGI) adapter - Thanks [@sarayourfriend](https://github.com/sarayourfriend) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/51?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.11.6...v1.12.0

[Changes][v1.12.0]


<a name="v1.11.6"></a>
# [version 1.11.6 (v1.11.6)](https://github.com/slackapi/bolt-python/releases/tag/v1.11.6) - 02 Mar 2022

### Changes

* [#608](https://github.com/slackapi/bolt-python/issues/608) Fix [#604](https://github.com/slackapi/bolt-python/issues/604) Respect the proxy_url in respond- Thanks [@seratch](https://github.com/seratch) [@gpiks](https://github.com/gpiks)

#### Document Updates

* [#609](https://github.com/slackapi/bolt-python/issues/609) Docs on handling options listeners with a filtering example - Thanks [@filmaj](https://github.com/filmaj) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/54?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.11.5...v1.11.6

[Changes][v1.11.6]


<a name="v1.11.5"></a>
# [version 1.11.5 (v1.11.5)](https://github.com/slackapi/bolt-python/releases/tag/v1.11.5) - 25 Feb 2022

### Changes

* [#602](https://github.com/slackapi/bolt-python/issues/602) Fix [#601](https://github.com/slackapi/bolt-python/issues/601) Allow for host option for AsyncSlackAppServer start method - Thanks [@seratch](https://github.com/seratch) [@ucgw](https://github.com/ucgw)
* [#588](https://github.com/slackapi/bolt-python/issues/588) Upgrade test dependencies & fix Falcon warning - Thanks [@seratch](https://github.com/seratch) 

#### Document Updates

* [#587](https://github.com/slackapi/bolt-python/issues/587) Update ngrok link to point to official guide - Thanks [@misscoded](https://github.com/misscoded) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/53?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.11.4...v1.11.5

[Changes][v1.11.5]


<a name="v1.11.4"></a>
# [version 1.11.4 (v1.11.4)](https://github.com/slackapi/bolt-python/releases/tag/v1.11.4) - 01 Feb 2022

### Changes

* [#586](https://github.com/slackapi/bolt-python/issues/586) Fix [#584](https://github.com/slackapi/bolt-python/issues/584) Wrong user_token assigned to new user (affected versions: v1.11.2, v1.11.3) - Thanks [@stantonius](https://github.com/stantonius) [@seratch](https://github.com/seratch)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/52?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.11.3...v1.11.4

[Changes][v1.11.4]


<a name="v1.11.3"></a>
# [version 1.11.3 (v1.11.3)](https://github.com/slackapi/bolt-python/releases/tag/v1.11.3) - 28 Jan 2022

### Changes

* [#580](https://github.com/slackapi/bolt-python/issues/580) Fix [#468](https://github.com/slackapi/bolt-python/issues/468) Replying with 0 results for a multi-select external option display previous successful results - Thanks [@seratch](https://github.com/seratch) [@prziborowski](https://github.com/prziborowski)
* [#581](https://github.com/slackapi/bolt-python/issues/581) Upgrade pytype version to the latest (2022.1.13) - Thanks [@seratch](https://github.com/seratch)
* [#578](https://github.com/slackapi/bolt-python/issues/578) Add more org-wide installation patterns to the SDK tests - Thanks [@seratch](https://github.com/seratch)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/50?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.11.2...v1.11.3

[Changes][v1.11.3]


<a name="v1.11.2"></a>
# [version 1.11.2 (v1.11.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.11.2) - 17 Jan 2022

### Changes

* [#576](https://github.com/slackapi/bolt-python/issues/576) Improve the built-in authorize for better support of user-scope only installations - Thanks [@seratch](https://github.com/seratch) 
* [#577](https://github.com/slackapi/bolt-python/issues/577) Fix [#561](https://github.com/slackapi/bolt-python/issues/561) matchers can be called even when app.message keyword does not match - Thanks [@seratch](https://github.com/seratch) [@caddac](https://github.com/caddac)

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/48?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.11.1...v1.11.2

[Changes][v1.11.2]


<a name="v1.11.1"></a>
# [version 1.11.1 (v1.11.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.11.1) - 24 Dec 2021

### Changes

* [#555](https://github.com/slackapi/bolt-python/issues/555) Fix [#552](https://github.com/slackapi/bolt-python/issues/552) Unable to use request body with lazy listener when socket mode is enabled - Thanks [@seratch](https://github.com/seratch) [@JordanGibson](https://github.com/JordanGibson) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/49?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.11.0...v1.11.1

[Changes][v1.11.1]


<a name="v1.11.0"></a>
# [version 1.11.0 (v1.11.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.11.0) - 14 Dec 2021

### Changes

* [#546](https://github.com/slackapi/bolt-python/issues/546) Fix [#545](https://github.com/slackapi/bolt-python/issues/545) Enable to use lazy listeners even when having any custom context data - Thanks [@seratch](https://github.com/seratch) 
* [#543](https://github.com/slackapi/bolt-python/issues/543) Fix url_verification error with the Flask adapter - Thanks [@seratch](https://github.com/seratch)
* [#544](https://github.com/slackapi/bolt-python/issues/544) Fix [#542](https://github.com/slackapi/bolt-python/issues/542) Add additional context values for FastAPI apps - Thanks [@kafejo](https://github.com/kafejo) [@seratch](https://github.com/seratch) 
* [#528](https://github.com/slackapi/bolt-python/issues/528) Add GitHub stale action for better triaging process - Thanks [@srajiang](https://github.com/srajiang) 
* [#547](https://github.com/slackapi/bolt-python/issues/547) Upgrade pytype, black versions - Thanks [@seratch](https://github.com/seratch) 

#### Document Updates

* [#519](https://github.com/slackapi/bolt-python/issues/519) [#518](https://github.com/slackapi/bolt-python/issues/518) An error in the HTTP mode Getting Started document (JP) - Thanks [@TORIFUKUKaiou](https://github.com/TORIFUKUKaiou) 
* [#523](https://github.com/slackapi/bolt-python/issues/523) Improve the Django app example to be more robust - Thanks [@seratch](https://github.com/seratch) 
* [#538](https://github.com/slackapi/bolt-python/issues/538) Update the respond utility guide - Thanks [@seratch](https://github.com/seratch) 
* [#541](https://github.com/slackapi/bolt-python/issues/541) Fix [#525](https://github.com/slackapi/bolt-python/issues/525) Japanese translation for [#524](https://github.com/slackapi/bolt-python/issues/524) (lazy listeners doc updates) - Thanks [@wongjas](https://github.com/wongjas) 
* [#534](https://github.com/slackapi/bolt-python/issues/534) Update link to view submissions doc  - Thanks [@wongjas](https://github.com/wongjas) 
* [#535](https://github.com/slackapi/bolt-python/issues/535) Fixes [#534](https://github.com/slackapi/bolt-python/issues/534), updates link to view submissions - Thanks [@wongjas](https://github.com/wongjas) 
* [#524](https://github.com/slackapi/bolt-python/issues/524) Update lazy lambda docs - Thanks [@srajiang](https://github.com/srajiang) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/42?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.10.0...v1.11.0

[Changes][v1.11.0]


<a name="v1.10.0"></a>
# [version 1.10.0 (v1.10.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.10.0) - 04 Nov 2021

### New Features

#### Improvement of Django ORM database connection management

Since this release, the Django adapter has been improved to properly manage the thread-local database connections bound to the threads managed by Bolt framework. If you use the Django adapter, we highly recommend upgrading to this version or newer.

Please refer to [#514](https://github.com/slackapi/bolt-python/issues/514) [#512](https://github.com/slackapi/bolt-python/issues/512) [#509](https://github.com/slackapi/bolt-python/issues/509) for more details.

### Changes

* [#514](https://github.com/slackapi/bolt-python/issues/514) [#512](https://github.com/slackapi/bolt-python/issues/512) [#509](https://github.com/slackapi/bolt-python/issues/509) Introduce ListenerStartHandler in the listener runner for better managing Django DB connections - Thanks [@ross](https://github.com/ross) [@seratch](https://github.com/seratch) 
* [#516](https://github.com/slackapi/bolt-python/issues/516) Improve the GitHub Actions job settings - Thanks [@seratch](https://github.com/seratch) 

#### Document Updates

* [#507](https://github.com/slackapi/bolt-python/issues/507) [#505](https://github.com/slackapi/bolt-python/issues/505) [#508](https://github.com/slackapi/bolt-python/issues/508) [#506](https://github.com/slackapi/bolt-python/issues/506)  Bunch of Japanese document updates - Thanks [@TORIFUKUKaiou](https://github.com/TORIFUKUKaiou) 
* [#500](https://github.com/slackapi/bolt-python/issues/500) Update OAuth link to point to JP docs instead of EN - Thanks [@wongjas](https://github.com/wongjas) 

### References

* Release Milestone: https://github.com/slackapi/bolt-python/milestone/47?closed=1
* All Diff: https://github.com/slackapi/bolt-python/compare/v1.9.4...v1.10.0

[Changes][v1.10.0]


<a name="v1.9.4"></a>
# [version 1.9.4 (v1.9.4)](https://github.com/slackapi/bolt-python/releases/tag/v1.9.4) - 29 Oct 2021

### Changes

* [#497](https://github.com/slackapi/bolt-python/issues/497) Add Python 3.10 to the supported versions - Thanks [@seratch](https://github.com/seratch) 
* [#503](https://github.com/slackapi/bolt-python/issues/503) Fix a bug in the asyncio based token rotation support - Thanks [@dkzk22](https://github.com/dkzk22) 
* [#504](https://github.com/slackapi/bolt-python/issues/504) Bump optional dependencies for v1.9.4 release  - Thanks [@seratch](https://github.com/seratch) 
* [#496](https://github.com/slackapi/bolt-python/issues/496) Upgrade pytype to the latest - Thanks [@seratch](https://github.com/seratch) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/46?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.9.3...v1.9.4

[Changes][v1.9.4]


<a name="v1.9.3"></a>
# [version 1.9.3 (v1.9.3)](https://github.com/slackapi/bolt-python/releases/tag/v1.9.3) - 13 Oct 2021

### Changes

* [#488](https://github.com/slackapi/bolt-python/issues/488) app.message listeners do not catch messages with subtype: thread_broadcast - Thanks [@seratch](https://github.com/seratch) [@kanny](https://github.com/kanny)

#### Document updates:

* Fix [#480](https://github.com/slackapi/bolt-python/issues/480) [#479](https://github.com/slackapi/bolt-python/issues/479) Adds updating views on submission for Japanese docs - Thanks [@wongjas](https://github.com/wongjas) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/45?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.9.2...v1.9.3

[Changes][v1.9.3]


<a name="v1.9.2"></a>
# [version 1.9.2 (v1.9.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.9.2) - 28 Sep 2021

### Changes

* [#477](https://github.com/slackapi/bolt-python/issues/477) Add more guide message in the HTML generated by the default failure handler - Thanks [@seratch](https://github.com/seratch) [@misscoded](https://github.com/misscoded) [@filmaj](https://github.com/filmaj) 
* [#476](https://github.com/slackapi/bolt-python/issues/476) Improve the error message in the case where AuthorizeResult is not found  - Thanks [@seratch](https://github.com/seratch) 

#### Document updates:

* [#479](https://github.com/slackapi/bolt-python/issues/479) Adds update view on submission docs - Thanks [@srajiang](https://github.com/srajiang) 
* [#472](https://github.com/slackapi/bolt-python/issues/472) update block id from listening modals  - Thanks [@bodepd](https://github.com/bodepd) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/44?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.9.1...v1.9.2

[Changes][v1.9.2]


<a name="v1.9.1"></a>
# [version 1.9.1 (v1.9.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.9.1) - 07 Sep 2021

### Changes

* [#460](https://github.com/slackapi/bolt-python/issues/460) Fix [#459](https://github.com/slackapi/bolt-python/issues/459) Invalid type hints in App / AsyncApp  - Thanks [@seratch](https://github.com/seratch) [@chrisbouchard](https://github.com/chrisbouchard)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/43?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.9.0...v1.9.1

[Changes][v1.9.1]


<a name="v1.9.0"></a>
# [version 1.9.0 (v1.9.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.9.0) - 31 Aug 2021

### New Features

#### More Customization for Apps

Since this release, developers can customize `listener_executor` in apps. Also, to support the use case where Enterprise Grid Org admins install apps from their app management page, we've added a new option to disable state parameter validation in the OAuth flow. Please note that we still don't recommend disabling the state validation for usual OAuth apps.

### Changes

* [#452](https://github.com/slackapi/bolt-python/issues/452) [#453](https://github.com/slackapi/bolt-python/issues/453) Enable to customize the `listener_executor` in `App` - Thanks [@chrisbouchard](https://github.com/chrisbouchard) 
* [#455](https://github.com/slackapi/bolt-python/issues/455) [#454](https://github.com/slackapi/bolt-python/issues/454) Add `oauth_settings.state_validation_enabled` to customize the OAuth flow  - Thanks [@seratch](https://github.com/seratch) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/41?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.8.1...v1.9.0

[Changes][v1.9.0]


<a name="v1.8.1"></a>
# [version 1.8.1 (v1.8.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.8.1) - 28 Aug 2021

### Changes

* [#451](https://github.com/slackapi/bolt-python/issues/451) Fix cookie extraction during OAuth for REST based AWS API GW + Lambda app - Thanks [@naveensan1](https://github.com/naveensan1) 
* [#449](https://github.com/slackapi/bolt-python/issues/449) Fix typo in `App` / `AsyncApp` comments and API documents - Thanks [@objectfox](https://github.com/objectfox) 
* [#446](https://github.com/slackapi/bolt-python/issues/446) Update the entity name - Thanks [@seratch](https://github.com/seratch) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/38?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.8.0...v1.8.1

[Changes][v1.8.1]


<a name="v1.8.0"></a>
# [version 1.8.0 (v1.8.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.8.0) - 13 Aug 2021

### Changes

* [#436](https://github.com/slackapi/bolt-python/issues/436) Fix [#409](https://github.com/slackapi/bolt-python/issues/409) Custom token rotation expiration time does not work if installation_store is passed at top level - Thanks [@seratch](https://github.com/seratch) 
* [#437](https://github.com/slackapi/bolt-python/issues/437) Fix a token rotation bug where a bot token is not refreshed if a user token does not exist - Thanks [@seratch](https://github.com/seratch)
* [#431](https://github.com/slackapi/bolt-python/issues/431) Fix [#430](https://github.com/slackapi/bolt-python/issues/430) by adding a new option to customize dev server (http.server) logging - Thanks [@seratch](https://github.com/seratch) [@cole-wilson](https://github.com/cole-wilson)
* [#432](https://github.com/slackapi/bolt-python/issues/432) Update Sanic adapter and its tests to be compatible with sanic v21  - Thanks [@seratch](https://github.com/seratch) 
* [#416](https://github.com/slackapi/bolt-python/issues/416) Fix type hint errors detected by pytype 2021.7.19 - Thanks [@seratch](https://github.com/seratch) 

#### Document Updates

* [#442](https://github.com/slackapi/bolt-python/issues/442) [#444](https://github.com/slackapi/bolt-python/issues/444) Added basic lazy lambda example setup and deploy instructions  - Thanks [@filmaj](https://github.com/filmaj) 
* [#418](https://github.com/slackapi/bolt-python/issues/418) [#414](https://github.com/slackapi/bolt-python/issues/414) Add Japanese translation of "token rotation" document - Thanks [@hirosassa](https://github.com/hirosassa) 
* [#426](https://github.com/slackapi/bolt-python/issues/426) [#406](https://github.com/slackapi/bolt-python/issues/406) Add Japanese translation of "Getting started over HTTP" and "Getting started" documents - Thanks [@hirosassa](https://github.com/hirosassa) 
* [#415](https://github.com/slackapi/bolt-python/issues/415) [#412](https://github.com/slackapi/bolt-python/issues/412) [#429](https://github.com/slackapi/bolt-python/issues/429) Update "incoming events" to "incoming requests" in documents - Thanks [@RhnSharma](https://github.com/RhnSharma) [@Shoryu-N](https://github.com/Shoryu-N) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/37?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.7.0...v1.8.0

[Changes][v1.8.0]


<a name="v1.8.0rc1"></a>
# [version 1.8.0rc1 (v1.8.0rc1)](https://github.com/slackapi/bolt-python/releases/tag/v1.8.0rc1) - 11 Aug 2021

Refer to [the v1.8.0 release note](https://github.com/slackapi/bolt-python/releases/tag/v1.8.0)

[Changes][v1.8.0rc1]


<a name="v1.7.0"></a>
# [version 1.7.0 (v1.7.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.7.0) - 15 Jul 2021

### New Features

### Token Rotation Support

This version includes the support for the apps enabling the newly released token rotation for better security. Refer to [the API document](https://api.slack.com/authentication/rotation) for the general information about the feature.

#### How to handle token rotation with this SDK

If you use any of the built-in `InstallationStore`, there is nothing else to change on your application code side. If you use the relational database tables along with a built-in `InstallationStore`, refer to the latest table schema [here](https://github.com/slackapi/python-slack-sdk/blob/v3.8.0/slack_sdk/oauth/installation_store/sqlalchemy/__init__.py#L34-L112).

If you use your own custom `authorize`, not the built-in `InstallationStoreAuthorize`, the `authorize` function needs to be updated to run the token rotation. Refer to the [`InstallationStoreAuthorize`'s code](https://github.com/slackapi/bolt-python/blob/v1.7.0/slack_bolt/authorization/authorize.py#L98-L268) to learn what to do for it.

#### Migration guide for Django users

If you operate Django apps based on [the example app in this repository](https://github.com/slackapi/bolt-python/tree/main/examples/django) and would like to enable token rotation for the apps, check [this commit](https://github.com/slackapi/bolt-python/commit/7920f3923a39b1d489c95d0ac34bd088e3081996) to learn the required changes for it.

#### Migration guide for `SQLAlchemyInstallationStore` users

If your app uses the built-in `SQLAlchemyInstallationStore` for managing Slack app installations, adding the following database columns is required for this version upgrade. Refer to [the code](https://github.com/slackapi/python-slack-sdk/tree/main/slack_sdk/oauth/installation_store/sqlalchemy) to check the complete ones. 

Also, since this version, all the table columns for string data have their max length for better compatibility with MySQL. We recommend setting the same ones for your models.

##### slack_installations

* `Column("bot_refresh_token", String(200)),`
* `Column("bot_token_expires_at", DateTime),`
* `Column("user_refresh_token", String(200)),`
* `Column("user_token_expires_at", DateTime),`

##### slack_bots

* `Column("bot_refresh_token", String(200)),`
* `Column("bot_token_expires_at", DateTime),`

### Changes

* [#404](https://github.com/slackapi/bolt-python/issues/404) Fix [#400](https://github.com/slackapi/bolt-python/issues/400) token rotation feature support - Thanks [@seratch](https://github.com/seratch)
* [#387](https://github.com/slackapi/bolt-python/issues/387) [#386](https://github.com/slackapi/bolt-python/issues/386) Replace re.search() with re.findall() in MessgeListenerMatches middleware to provide better matching results - Thanks [@albeec13](https://github.com/albeec13) 
* [#379](https://github.com/slackapi/bolt-python/issues/379) Make cookies extraction on AWS Lambda compatible with its format v1.0 - Thanks [@tattee](https://github.com/tattee)
* [#375](https://github.com/slackapi/bolt-python/issues/375) Update install page to avoid favicon downloads - Thanks [@Bhavya6187](https://github.com/Bhavya6187)
* [#401](https://github.com/slackapi/bolt-python/issues/401) Fix [#378](https://github.com/slackapi/bolt-python/issues/378) by adding middleware error handlers - Thanks [@seratch](https://github.com/seratch) [@jeremyschulman](https://github.com/jeremyschulman) 
* [#403](https://github.com/slackapi/bolt-python/issues/403) Fix [#377](https://github.com/slackapi/bolt-python/issues/377) Better log messages for AsyncApp when a listener is missing - Thanks [@seratch](https://github.com/seratch)
* [#394](https://github.com/slackapi/bolt-python/issues/394) Fix [#370](https://github.com/slackapi/bolt-python/issues/370) by adding an alias of next arg (next_) in middleware arguments - Thanks [@seratch](https://github.com/seratch)
* [#402](https://github.com/slackapi/bolt-python/issues/402) Fix [#372](https://github.com/slackapi/bolt-python/issues/372) by adding listener matcher docs - Thanks [@seratch](https://github.com/seratch)
* [#389](https://github.com/slackapi/bolt-python/issues/389) Add reference to WorkflowStepBuilder in docs - Thanks [@misscoded](https://github.com/misscoded)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/35?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.6.1...v1.7.0


[Changes][v1.7.0]


<a name="v1.6.1"></a>
# [version 1.6.1 (v1.6.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.6.1) - 03 Jun 2021

### Changes

* [#331](https://github.com/slackapi/bolt-python/issues/331) [#330](https://github.com/slackapi/bolt-python/issues/330) Potentially request.body can be None when using a custom adapter  - Thanks [@matteobaldelli](https://github.com/matteobaldelli) [@seratch](https://github.com/seratch)
* [#363](https://github.com/slackapi/bolt-python/issues/363) Fix [#346](https://github.com/slackapi/bolt-python/issues/346) Allow unfurl_media / unfurl_links in ack / respond  - Thanks [@gburek-fastly](https://github.com/gburek-fastly) [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/36?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.6.0...v1.6.1

[Changes][v1.6.1]


<a name="v1.6.0"></a>
# [version 1.6.0 (v1.6.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.6.0) - 07 May 2021

### New Features

#### Code Suggestion for Missing Listeners

Since this version, the warning message for unhandled requests is even more helpful!

Let's say you've configured the "message" event subscription in the Slack App configuration page, and the Slack server-side started sending message events to your app. However, your app does not have the corresponding event listener yet. In this case, Bolt suggests the missing listener with a working code snippet.

```
WARNING:slack_bolt.App:Unhandled request ({'type': 'event_callback', 'event': {'type': 'message'}})
---
[Suggestion] You can handle this type of event with the following listener function:

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
```

The new suggestion logging should be helpful for the developers who are new to Bolt and the Slack platform.

#### Options For Turning the Built-in Middleware Off

Developers can turn any of the built-in middleware off if they would like to do so for some reason.

```python
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # Verify request signature
    request_verification_enabled = False,  # default: True
    # Skip processing the events generated by this app's bot user itself
    ignoring_self_events_enabled = False,  # default: True
    # Respond to ssl_check requests
    ssl_check_enabled = False,  # default: True
    # Respond to url_verification requests in the Events API configuration steps
    url_verification_enabled = False,  # default: True
)
```

Please make sure if it's safe enough when you turn a built-in middleware off. **We strongly recommend using `RequestVerification` for better security**. If you have a proxy that verifies request signature in front of the Bolt app, it's totally fine to disable `RequestVerification` to avoid duplication of work. Don't turn it off just for easiness of development.

### Changes

* [#323](https://github.com/slackapi/bolt-python/issues/323) Add missing listener suggestion to the default unhandled error message - Thanks [@seratch](https://github.com/seratch)
* [#310](https://github.com/slackapi/bolt-python/issues/310) Fix [#307](https://github.com/slackapi/bolt-python/issues/307) Add options to disable the built-in middleware - Thanks [@seratch](https://github.com/seratch) [@hubhanker99](https://github.com/hubhanker99)
* [#311](https://github.com/slackapi/bolt-python/issues/311) Fix [#309](https://github.com/slackapi/bolt-python/issues/309) Fallback to no-emoji boot message on any platforms - Thanks [@seratch](https://github.com/seratch) [@christheodosius](https://github.com/christheodosius)
* [#315](https://github.com/slackapi/bolt-python/issues/315) [#316](https://github.com/slackapi/bolt-python/issues/316) Fix Chalice deployment failures caused by [#270](https://github.com/slackapi/bolt-python/issues/270) - Thanks [@jlujan-invitae](https://github.com/jlujan-invitae)
* [#313](https://github.com/slackapi/bolt-python/issues/313) Fix [#312](https://github.com/slackapi/bolt-python/issues/312) Type hint errors with pytype 2021.4.26  - Thanks [@seratch](https://github.com/seratch) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/34?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.5.0...v1.6.0


[Changes][v1.6.0]


<a name="v1.5.0"></a>
# [version 1.5.0 (v1.5.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.5.0) - 20 Apr 2021

### New Features

#### Underlying SDK Upgrade

This release upgrades the underlying `slack-sdk` package from 3.4 to 3.5 (or higher). Refer to the package's release note for more details: https://github.com/slackapi/python-slack-sdk/releases/tag/v3.5.0

#### Built-in Token Revocation Handlers

Since this version, the out-of-the-box support for the following events is available:

* https://api.slack.com/events/tokens_revoked
* https://api.slack.com/events/app_uninstalled

To use this feature, all you need to do are:
* Enable `installation_store` of the OAuth settings (see [the document](/concepts/authenticating-oauth))
* Call `enable_token_revocation_listeners()` method of the `App` / `AsyncApp` instance

```python
app = App(
  # Enabling installation_store required
)
app.enable_token_revocation_listeners()
```

This is equivalent to the following code:

```python
app = App()  # installation_store required
app.event("tokens_revoked")(app.default_tokens_revoked_event_listener)
app.event("app_uninstalled")(app.default_app_uninstalled_event_listener)
```

These event listeners properly utilize the data deletion methods in the `InstallationStore` you use. If you have your own `InstallationStore` implementation, please implement deletion methods in the classes. Refer to https://github.com/slackapi/python-slack-sdk/pull/995 for more details.

#### Customize Unhandled Error Handling

Handling unmatched request patterns had not been customizable in the past versions. The pull request [#290](https://github.com/slackapi/bolt-python/issues/290) introduced a new option to enable using `@app.error` handlers for unmatched requests. The default is set to False, which is fully backward compatible. If the option is True, Bolt raises a `BoltUnhandledRequestError` with sufficient information. `@app.error` handler can customize the behavior for the patterns (e.g., having custom logging, changing HTTP status from 404 to something else).

```python
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # enable @app.error handler to catch the patterns
    raise_error_for_unhandled_request=True,
)

@app.error
def handle_errors(error):
    if isinstance(error, BoltUnhandledRequestError):
        # You may want to have debug/info logging here
        return BoltResponse(status=200, body="")
    else:
        # other error patterns
        return BoltResponse(status=500, body="Something wrong")
```


#### Add `respond` to `app.view` Listeners

When an input block in your modal has `response_url_enabled: true`, `view_submission` payloads can have `response_urls`. Since this version, you can use `respond` utility to use the primary element in the array.

```python
@app.view("view-id")
def check(ack, respond):
    # if there is an input block with response_url_enabled: true
    respond("This message will be posted in the selected channel")
    ack()
```

see also:
* https://api.slack.com/reference/block-kit/block-elements#conversation_select
* https://github.com/slackapi/bolt-python/pull/288

#### Better Compatibility with Thread-local feature based Libraries

`ListenerCompletionHandler` is a new addition, which enables developers to customize callbacks for listener runner completion. The callbacks can be useful, especially when you use a library/framework that utilizes thread-local variables (e.g., Django ORM, thread-local sessions in SQLAlchemy) along with Bolt for Python. 

If you're interested in how it works, check the updated Django adapter implementation for details: https://github.com/slackapi/bolt-python/blob/v1.5.0/slack_bolt/adapter/django/handler.py

```python
from django.db import connections

class DjangoListenerCompletionHandler(ListenerCompletionHandler):
    def handle(self, request: BoltRequest, response: Optional[BoltResponse]) -> None:
        # closes all the thread-local connections in the current thread
        connections.close_all()
```

### Changes

* [#270](https://github.com/slackapi/bolt-python/issues/270) Add support for lazy listeners when running with chalice local  - Thanks [@jlujan-invitae](https://github.com/jlujan-invitae)
* [#281](https://github.com/slackapi/bolt-python/issues/281) Fix [#280](https://github.com/slackapi/bolt-python/issues/280) Django thread-local connection cleanup in multi threads - Thanks [@seratch](https://github.com/seratch) 
* [#287](https://github.com/slackapi/bolt-python/issues/287) Enable installation_store authorize to fallback to bots (prep for [#254](https://github.com/slackapi/bolt-python/issues/254)) - Thanks [@seratch](https://github.com/seratch) 
* [#289](https://github.com/slackapi/bolt-python/issues/289) Fix [#254](https://github.com/slackapi/bolt-python/issues/254) Add built-in tokens_revoked/app_uninstalled event handlers - Thanks [@seratch](https://github.com/seratch) 
* [#288](https://github.com/slackapi/bolt-python/issues/288) Fix [#260](https://github.com/slackapi/bolt-python/issues/260) Enable to use respond utility in app.view listeners (only when response_urls exists) - Thanks [@seratch](https://github.com/seratch) 
* [#290](https://github.com/slackapi/bolt-python/issues/290) Fix [#273](https://github.com/slackapi/bolt-python/issues/273) Enable developers to customize the way to handle unmatched requests - Thanks [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/33?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.4.4...v1.5.0


[Changes][v1.5.0]


<a name="v1.4.4"></a>
# [version 1.4.4 (v1.4.4)](https://github.com/slackapi/bolt-python/releases/tag/v1.4.4) - 22 Mar 2021

### Changes

* [#261](https://github.com/slackapi/bolt-python/issues/261) [#262](https://github.com/slackapi/bolt-python/issues/262) SocketModeHandler#start() does not terminate on Windows - Thanks [@vv-grinko](https://github.com/vv-grinko) [@seratch](https://github.com/seratch) 
* [#256](https://github.com/slackapi/bolt-python/issues/256) [#257](https://github.com/slackapi/bolt-python/issues/257) Improve the warning message in App/AsyncApp constructor - Thanks [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/32?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.4.3...v1.4.4


[Changes][v1.4.4]


<a name="v1.4.3"></a>
# [version 1.4.3 (v1.4.3)](https://github.com/slackapi/bolt-python/releases/tag/v1.4.3) - 06 Mar 2021

### Changes

* [#251](https://github.com/slackapi/bolt-python/issues/251) [#253](https://github.com/slackapi/bolt-python/issues/253) Unable to run OAuth flow URLs in Google Cloud Run - Thanks [@gifflarn](https://github.com/gifflarn) [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/31?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.4.2...v1.4.3


[Changes][v1.4.3]


<a name="v1.4.2"></a>
# [version 1.4.2 (v1.4.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.4.2) - 03 Mar 2021

### Changes

* [#246](https://github.com/slackapi/bolt-python/issues/246) Pass the Bolt logger in default WebClient instantiation - Thanks [@seratch](https://github.com/seratch)
* Upgrade the minimum version of underlying `slack_sdk` to v3.4.1 - Thanks [@seratch](https://github.com/seratch) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/30?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.4.1...v1.4.2


[Changes][v1.4.2]


<a name="v1.4.1"></a>
# [version 1.4.1 (v1.4.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.4.1) - 21 Feb 2021

### Changes

* [#244](https://github.com/slackapi/bolt-python/issues/244) Fix an issue where different user's token may exist in context  - Thanks [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/29?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.4.0...v1.4.1


[Changes][v1.4.1]


<a name="v1.4.0"></a>
# [version 1.4.0 (v1.4.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.4.0) - 19 Feb 2021

This release upgrades the underlying `slack-sdk` package from 3.3 to 3.4 (or higher). Refer to the package's release note for more details: https://github.com/slackapi/python-slack-sdk/releases/tag/v3.4.0

### Changes

* [#243](https://github.com/slackapi/bolt-python/issues/243) Upgrade slack-sdk to 3.4 - Thanks [@seratch](https://github.com/seratch) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/21?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.3.2...v1.4.0


[Changes][v1.4.0]


<a name="v1.3.2"></a>
# [version 1.3.2 (v1.3.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.3.2) - 11 Feb 2021

### Changes

This patch version upgrades the minimum slack-sdk version from 3.3.1 to 3.3.2 for proxy issue in the built-in SocketModeClient. Also, Socket Mode adapter supports newly added `proxy_headers` argument in its constructor. Refer to https://github.com/slackapi/python-slack-sdk/releases/tag/v3.3.2 for the underlying changes.

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/27?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.3.1...v1.3.2


[Changes][v1.3.2]


<a name="v1.3.1"></a>
# [version 1.3.1 (v1.3.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.3.1) - 09 Feb 2021

### Changes

* [#232](https://github.com/slackapi/bolt-python/issues/232) [#233](https://github.com/slackapi/bolt-python/issues/233) Unmatched message listener middleware can be called - Thanks [@Beartime234](https://github.com/Beartime234) [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/26?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.3.0...v1.3.1


[Changes][v1.3.1]


<a name="v1.3.0"></a>
# [version 1.3.0 (v1.3.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.3.0) - 05 Feb 2021

This release upgrades the underlying `slack-sdk` package from 3.2 to 3.3. Refer to the package's release note for more details: https://github.com/slackapi/python-slack-sdk/releases/tag/v3.3.0

### Changes

* Upgrade `slack-sdk` from 3.2 to 3.3 - Thanks [@seratch](https://github.com/seratch)
* [#224](https://github.com/slackapi/bolt-python/issues/224) [#113](https://github.com/slackapi/bolt-python/issues/113) Workflow steps decorator - Thanks [@seratch](https://github.com/seratch) 
* [#220](https://github.com/slackapi/bolt-python/issues/220) Correct Event API document - Thanks [@mwbrooks](https://github.com/mwbrooks) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/14?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.2.3...v1.3.0


[Changes][v1.3.0]


<a name="v1.2.3"></a>
# [version 1.2.3 (v1.2.3)](https://github.com/slackapi/bolt-python/releases/tag/v1.2.3) - 20 Jan 2021

### Changes

* [#215](https://github.com/slackapi/bolt-python/issues/215) [#216](https://github.com/slackapi/bolt-python/issues/216) [#217](https://github.com/slackapi/bolt-python/issues/217) Using callable object instances as middleware does not work - Thanks [@nickovs](https://github.com/nickovs)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/24?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.2.2...v1.2.3


[Changes][v1.2.3]


<a name="v1.2.2"></a>
# [version 1.2.2 (v1.2.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.2.2) - 19 Jan 2021

### Changes

* [#199](https://github.com/slackapi/bolt-python/issues/199) [#201](https://github.com/slackapi/bolt-python/issues/201) Improvement related to [#199](https://github.com/slackapi/bolt-python/issues/199): add event type name validation - Thanks [@cgamio](https://github.com/cgamio) [@seratch](https://github.com/seratch) 
* [#212](https://github.com/slackapi/bolt-python/issues/212) [#208](https://github.com/slackapi/bolt-python/issues/208) AsyncOAuthFlow run_installation missing team_name and enterprise_name fields in returned Installation - Thanks [@jwelch92](https://github.com/jwelch92) [@seratch](https://github.com/seratch)
* [#213](https://github.com/slackapi/bolt-python/issues/213) [#210](https://github.com/slackapi/bolt-python/issues/210) AsyncOAuthSettings uses CallbackOptions instead of AsyncCallbackOptions - Thanks [@jwelch92](https://github.com/jwelch92) [@seratch](https://github.com/seratch)
### References

* milestone: https://github.com/slackapi/bolt-python/milestone/20?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.2.1...v1.2.2


[Changes][v1.2.2]


<a name="v1.2.1"></a>
# [version 1.2.1 (v1.2.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.2.1) - 12 Jan 2021

### Changes

* [#203](https://github.com/slackapi/bolt-python/issues/203) Fix [#198](https://github.com/slackapi/bolt-python/issues/198) bug where str subtype constraint does not work - Thanks [@seratch](https://github.com/seratch) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/23?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.2.0...v1.2.1


[Changes][v1.2.1]


<a name="v1.2.0"></a>
# [version 1.2.0 (v1.2.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.2.0) - 12 Jan 2021

### New Features

#### Socket Mode

This version includes support for Socket Mode, which enables developers to receive interactivy payalods and events through WebSocket connections. 

https://api.slack.com/socket-mode

For WebSocket connection handling, there are four implementations including major 3rd party open-source libraries.

|PyPI Project|Bolt Adapter|
|-|-|
|[skack_sdk](https://pypi.org/project/skack-sdk/)|[slack_bolt.adapter.socket_mode.SocketModeHandler](https://github.com/slackapi/bolt-python/blob/v1.2.0/slack_bolt/adapter/socket_mode/)|
|[websocket_client](https://pypi.org/project/websocket_client/)|[slack_bolt.adapter.socket_mode.websocket_client.SocketModeHandler](https://github.com/slackapi/bolt-python/blob/v1.2.0/slack_bolt/adapter/socket_mode/websocket_client/)|
|[aiohttp](https://pypi.org/project/aiohttp/) (asyncio-based)|[slack_bolt.adapter.socket_mode.aiohttp.AsyncSocketModeHandler](https://github.com/slackapi/bolt-python/blob/v1.2.0/slack_bolt/adapter/socket_mode/aiohttp/)|
|[websockets](https://pypi.org/project/websockets/) (asyncio-based)|[slack_bolt.adapter.socket_mode.websockets.AsyncSocketModeHandler](https://github.com/slackapi/bolt-python/blob/v1.2.0/slack_bolt/adapter/socket_mode/websockets/)|

Here is a minimal working example with the built-in WebSocket client. You can switch to other implementation by changing the imports and adding the extra dependencies (websocket_client, aiohttp, websockets).

```python
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])

if __name__ == "__main__":
    # export SLACK_APP_TOKEN=xapp-***
    # export SLACK_BOT_TOKEN=xoxb-***
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

If you want to use asyncio for everything, you can use `aiohttp` or `websockets` (along with aiohttp for `AsyncWebClient`). `AsyncSocketModeHandler` requires all of your middleware/listeners to be compatible with the async/await programming style.

```python
from slack_bolt.app.async_app import AsyncApp
# The default is the aiohttp based implementation
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```


### Changes

* [#108](https://github.com/slackapi/bolt-python/issues/108) [#160](https://github.com/slackapi/bolt-python/issues/160) [#176](https://github.com/slackapi/bolt-python/issues/176) [#159](https://github.com/slackapi/bolt-python/issues/159) [#200](https://github.com/slackapi/bolt-python/issues/200) Socket Mode support - Thanks [@seratch](https://github.com/seratch) [@stevegill](https://github.com/stevegill)
* [#174](https://github.com/slackapi/bolt-python/issues/174) [#192](https://github.com/slackapi/bolt-python/issues/192) [#202](https://github.com/slackapi/bolt-python/issues/202) Enable using class/instance methods for middleware/listners - Thanks [@liuyangc3](https://github.com/liuyangc3) [@seratch](https://github.com/seratch)
* [#197](https://github.com/slackapi/bolt-python/issues/197) [#198](https://github.com/slackapi/bolt-python/issues/198) Fix a bug where bot messages from class apps won't be passed to app.message listeners - Thanks [@uc-dang-tiki](https://github.com/uc-dang-tiki) [@seratch](https://github.com/seratch)
* [#186](https://github.com/slackapi/bolt-python/issues/186) [#183](https://github.com/slackapi/bolt-python/issues/183) Add an easier way to configure the direct install URL on App Directory

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/12?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.1.5...v1.2.0


[Changes][v1.2.0]


<a name="v1.1.5"></a>
# [version 1.1.5 (v1.1.5)](https://github.com/slackapi/bolt-python/releases/tag/v1.1.5) - 07 Jan 2021

### Changes

* [#194](https://github.com/slackapi/bolt-python/issues/194) Fix [#193](https://github.com/slackapi/bolt-python/issues/193) by enabling listener middleware to return a response - Thanks [@Ambro17](https://github.com/Ambro17) [@seratch](https://github.com/seratch) 
* [#189](https://github.com/slackapi/bolt-python/issues/189) Add type hint updates missed in [#148](https://github.com/slackapi/bolt-python/issues/148)  - Thanks [@seratch](https://github.com/seratch) 
* Upgrade `slack_sdk` to v3.1.1 - Thanks [@seratch](https://github.com/seratch) 

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/19?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.1.4...v1.1.5


[Changes][v1.1.5]


<a name="v1.1.4"></a>
# [version 1.1.4 (v1.1.4)](https://github.com/slackapi/bolt-python/releases/tag/v1.1.4) - 19 Dec 2020

### Changes

* [#180](https://github.com/slackapi/bolt-python/issues/180) Fix [#158](https://github.com/slackapi/bolt-python/issues/158) by adding token_verification_enabled option to App - Thanks [@seratch](https://github.com/seratch)
* [#167](https://github.com/slackapi/bolt-python/issues/167) Upgrade black (code formatter) to the latest version - Thanks [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/18?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.1.3...v1.1.4


[Changes][v1.1.4]


<a name="v1.1.3"></a>
# [version 1.1.3 (v1.1.3)](https://github.com/slackapi/bolt-python/releases/tag/v1.1.3) - 16 Dec 2020

This patch version is a hotfix release for v1.1.2. If you use `installation_store_bot_only` option, please upgrade to this version.

### Changes

* [#177](https://github.com/slackapi/bolt-python/issues/177) [#178](https://github.com/slackapi/bolt-python/issues/178) Enable to use installation_store_bot_only flag not only as the top-level arg  - Thanks [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/17?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.1.2...v1.1.3


[Changes][v1.1.3]


<a name="v1.1.2"></a>
# [version 1.1.2 (v1.1.2)](https://github.com/slackapi/bolt-python/releases/tag/v1.1.2) - 08 Dec 2020

### New Features

#### v1.0 authorize compatible mode

Now you can use InstallationStore's v1.0 compatible mode in authorize. 

Setting `App`/`AsyncApp`'s `installation_store_bot_only` constructor argument as True works in the same manner as v1.0 authorize. If you manually initialize `InstallationStoreAuthorize`, `bot_only` flag in it is the one you can configure. See the pull request [#171](https://github.com/slackapi/bolt-python/issues/171) for more details.

```python
installation_store = MyInstallationStore()
oauth_state_store = MyOAuthStateStore()

app = App(
    # If you want to keep using only `#find_bot` for token retrieval,
    # you can configure installation_store_bot_only as True
    installation_store_bot_only=True,
    oauth_settings=OAuthSettings(
        installation_store=installation_store,
        state_store=oauth_state_store,
    ),
)
```

**NOTE:** If you use `installation_store_bot_only` flag in `OAuthFlow` or `OAuthSettings`, please upgrade to v1.1.3 or higher.

### Changes

* [#171](https://github.com/slackapi/bolt-python/issues/171) Add v1.0 compatible mode to [#148](https://github.com/slackapi/bolt-python/issues/148) Org-wide App support  - Thanks [@seratch](https://github.com/seratch)
* [#173](https://github.com/slackapi/bolt-python/issues/173) [#170](https://github.com/slackapi/bolt-python/issues/170) Remove the possibility of issue [#170](https://github.com/slackapi/bolt-python/issues/170) by removing emoji from the boot message only for Windows - Thanks [@athifongoqa](https://github.com/athifongoqa) [@seratch](https://github.com/seratch)
* [#172](https://github.com/slackapi/bolt-python/issues/172) Fix Django app example to run with v1.1 - Thanks [@vokey](https://github.com/vokey)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/16?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.1.1...v1.1.2

[Changes][v1.1.2]


<a name="v1.1.1"></a>
# [version 1.1.1 (v1.1.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.1.1) - 03 Dec 2020

### Changes

* [#165](https://github.com/slackapi/bolt-python/issues/165) [#168](https://github.com/slackapi/bolt-python/issues/168) Provide a way to easily use aiohttp-devtools for AsyncApp apps - Thanks [@stevegill](https://github.com/stevegill) [@seratch](https://github.com/seratch)
* [#169](https://github.com/slackapi/bolt-python/issues/169) Improve request parser to safely extract values from payloads in any case - Thanks [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/15?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.1.0...v1.1.1


[Changes][v1.1.1]


<a name="v1.1.0"></a>
# [version 1.1.0 (v1.1.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.1.0) - 02 Dec 2020

### New Features

#### Org-Wide App Installation Support

This version includes the changes related to Org-Wide App feature, which is for Enterprise Grid organizations.

https://api.slack.com/enterprise/apps

Refer to the Python Slack SDK's release note for details: https://github.com/slackapi/python-slack-sdk/releases/tag/v3.1.0

As long as the changes on the low-level SDK side does not affect your apps, most of existing Bolt apps do not require any updates in code. If you are an existing user of either of `AmazonS3InstallationStore` or `FileInstallationStore`, please upgrade to v1.1.3 or higher and set `installation_store_bot_only` flag as `True` in `App`/`AsyncApp` constructor. See [v1.1.2 release note](https://github.com/slackapi/bolt-python/releases/tag/v1.1.2) for details.

### Changes

* [#148](https://github.com/slackapi/bolt-python/issues/148) Add Org-Wide App Installation Support - Thanks [@stevegill](https://github.com/stevegill) [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/9?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.0.1...v1.1.0


[Changes][v1.1.0]


<a name="v1.1.0rc1"></a>
# [version 1.1.0 RC1 (v1.1.0rc1)](https://github.com/slackapi/bolt-python/releases/tag/v1.1.0rc1) - 01 Dec 2020

See v1.1.0 release note.

[Changes][v1.1.0rc1]


<a name="v1.0.1"></a>
# [version 1.0.1 (v1.0.1)](https://github.com/slackapi/bolt-python/releases/tag/v1.0.1) - 24 Nov 2020

### Changes

* [#152](https://github.com/slackapi/bolt-python/issues/152) Fix Events API handling issue in shared channels - Thanks [@seratch](https://github.com/seratch)
* [#153](https://github.com/slackapi/bolt-python/issues/153) Add OAuth related arg validation and flexibility - Thanks [@seratch](https://github.com/seratch)
* [#154](https://github.com/slackapi/bolt-python/issues/154) Apply internal adjustments for Socket Mode support - Thanks [@seratch](https://github.com/seratch)

### References

* milestone: https://github.com/slackapi/bolt-python/milestone/13?closed=1
* diff: https://github.com/slackapi/bolt-python/compare/v1.0.0...v1.0.1

[Changes][v1.0.1]


<a name="v1.0.0"></a>
# [version 1.0.0 (v1.0.0)](https://github.com/slackapi/bolt-python/releases/tag/v1.0.0) - 09 Nov 2020

Here is the first stable version of [Bolt for Python](https://pypi.org/project/slack-bolt/) 🎉 

This framework has been carefully designed to be easy and intuitive for Python developers while aligning with the existing Bolt frameworks. If you’re a Pythonista, we think you’ll like it!

You can start with `pip install slack_bolt` and [the Getting Started Guide](https://slack.dev/bolt-python/tutorial/getting-started). To learn more, check the following resources:

* [The Bolt family of SDKs](https://api.slack.com/tools/bolt)
* [Bolt for Python website](https://slack.dev/bolt-python/)
* [Examples](https://github.com/slackapi/bolt-python/tree/v1.0.0/examples)

[Changes][v1.0.0]


<a name="v1.0.0rc2"></a>
# [version 1.0.0 RC2 (v1.0.0rc2)](https://github.com/slackapi/bolt-python/releases/tag/v1.0.0rc2) - 07 Nov 2020

This is the latest release candidate version of [slack_bolt](https://pypi.org/project/slack-bolt/) v1.0.0.

* [The Bolt family of SDKs](https://api.slack.com/tools/bolt)
* [Bolt for Python website](https://slack.dev/bolt-python/)

We will be releasing v1.0.0 within a few days. Thank you very much for all the contributions and feedback from the community!

[Changes][v1.0.0rc2]


<a name="v1.0.0rc1"></a>
# [version 1.0.0 RC1 (v1.0.0rc1)](https://github.com/slackapi/bolt-python/releases/tag/v1.0.0rc1) - 06 Nov 2020

This is the first release candidate version of [slack_bolt](https://pypi.org/project/slack-bolt/) v1.0.0.

* [The Bolt family of SDKs](https://api.slack.com/tools/bolt)
* [Bolt for Python website](https://slack.dev/bolt-python/)

We will be releasing v1.0.0 within a few days. Thank you very much for all the contributions and feedback from the community!

[Changes][v1.0.0rc1]


<a name="v0.9.6b0"></a>
# [version 0.9.6 beta (v0.9.6b0)](https://github.com/slackapi/bolt-python/releases/tag/v0.9.6b0) - 29 Oct 2020



[Changes][v0.9.6b0]


<a name="v0.9.5b0"></a>
# [version 0.9.5 beta (v0.9.5b0)](https://github.com/slackapi/bolt-python/releases/tag/v0.9.5b0) - 27 Oct 2020



[Changes][v0.9.5b0]


<a name="v0.9.4b0"></a>
# [version 0.9.4 beta (v0.9.4b0)](https://github.com/slackapi/bolt-python/releases/tag/v0.9.4b0) - 22 Oct 2020



[Changes][v0.9.4b0]


<a name="v0.9.3b0"></a>
# [version 0.9.3 beta (v0.9.3b0)](https://github.com/slackapi/bolt-python/releases/tag/v0.9.3b0) - 16 Oct 2020



[Changes][v0.9.3b0]


<a name="v0.9.2b0"></a>
# [version 0.9.2 beta (v0.9.2b0)](https://github.com/slackapi/bolt-python/releases/tag/v0.9.2b0) - 06 Oct 2020

https://github.com/slackapi/bolt-python/milestone/7?closed=1

[Changes][v0.9.2b0]


<a name="v0.9.1b0"></a>
# [version 0.9.1 beta (v0.9.1b0)](https://github.com/slackapi/bolt-python/releases/tag/v0.9.1b0) - 04 Oct 2020

https://github.com/slackapi/bolt-python/milestone/6?closed=1

[Changes][v0.9.1b0]


<a name="v0.9.0b0"></a>
# [version 0.9.0 beta (v0.9.0b0)](https://github.com/slackapi/bolt-python/releases/tag/v0.9.0b0) - 01 Oct 2020

v0.9.0b0 is the first beta release of Bolt for Python. All the latest Slack Platform features are supported 🎉 

https://github.com/slackapi/bolt-python/milestone/3?closed=1

[Changes][v0.9.0b0]


[v1.19.1]: https://github.com/slackapi/bolt-python/compare/v1.19.0...v1.19.1
[v1.19.0]: https://github.com/slackapi/bolt-python/compare/v1.19.0rc1...v1.19.0
[v1.19.0rc1]: https://github.com/slackapi/bolt-python/compare/v1.18.1...v1.19.0rc1
[v1.18.1]: https://github.com/slackapi/bolt-python/compare/v1.18.0...v1.18.1
[v1.18.0]: https://github.com/slackapi/bolt-python/compare/v1.17.2...v1.18.0
[v1.17.2]: https://github.com/slackapi/bolt-python/compare/v1.17.1...v1.17.2
[v1.17.1]: https://github.com/slackapi/bolt-python/compare/v1.17.0...v1.17.1
[v1.17.0]: https://github.com/slackapi/bolt-python/compare/v1.17.0rc4...v1.17.0
[v1.17.0rc4]: https://github.com/slackapi/bolt-python/compare/v1.17.0rc3...v1.17.0rc4
[v1.17.0rc3]: https://github.com/slackapi/bolt-python/compare/v1.17.0rc2...v1.17.0rc3
[v1.17.0rc2]: https://github.com/slackapi/bolt-python/compare/v1.17.0rc1...v1.17.0rc2
[v1.17.0rc1]: https://github.com/slackapi/bolt-python/compare/v1.16.4...v1.17.0rc1
[v1.16.4]: https://github.com/slackapi/bolt-python/compare/v1.16.3...v1.16.4
[v1.16.3]: https://github.com/slackapi/bolt-python/compare/v1.16.2...v1.16.3
[v1.16.2]: https://github.com/slackapi/bolt-python/compare/v1.16.1...v1.16.2
[v1.16.1]: https://github.com/slackapi/bolt-python/compare/v1.16.0...v1.16.1
[v1.16.0]: https://github.com/slackapi/bolt-python/compare/v1.15.5...v1.16.0
[v1.15.5]: https://github.com/slackapi/bolt-python/compare/v1.15.4...v1.15.5
[v1.15.4]: https://github.com/slackapi/bolt-python/compare/v1.15.3...v1.15.4
[v1.15.3]: https://github.com/slackapi/bolt-python/compare/v1.15.2...v1.15.3
[v1.15.2]: https://github.com/slackapi/bolt-python/compare/v1.15.1...v1.15.2
[v1.15.1]: https://github.com/slackapi/bolt-python/compare/v1.15.0...v1.15.1
[v1.15.0]: https://github.com/slackapi/bolt-python/compare/v1.14.3...v1.15.0
[v1.14.3]: https://github.com/slackapi/bolt-python/compare/v1.14.2...v1.14.3
[v1.14.2]: https://github.com/slackapi/bolt-python/compare/v1.14.1...v1.14.2
[v1.14.1]: https://github.com/slackapi/bolt-python/compare/v1.14.0...v1.14.1
[v1.14.0]: https://github.com/slackapi/bolt-python/compare/v1.13.2...v1.14.0
[v1.13.2]: https://github.com/slackapi/bolt-python/compare/v1.13.1...v1.13.2
[v1.13.1]: https://github.com/slackapi/bolt-python/compare/v1.13.0...v1.13.1
[v1.13.0]: https://github.com/slackapi/bolt-python/compare/v1.12.0...v1.13.0
[v1.12.0]: https://github.com/slackapi/bolt-python/compare/v1.11.6...v1.12.0
[v1.11.6]: https://github.com/slackapi/bolt-python/compare/v1.11.5...v1.11.6
[v1.11.5]: https://github.com/slackapi/bolt-python/compare/v1.11.4...v1.11.5
[v1.11.4]: https://github.com/slackapi/bolt-python/compare/v1.11.3...v1.11.4
[v1.11.3]: https://github.com/slackapi/bolt-python/compare/v1.11.2...v1.11.3
[v1.11.2]: https://github.com/slackapi/bolt-python/compare/v1.11.1...v1.11.2
[v1.11.1]: https://github.com/slackapi/bolt-python/compare/v1.11.0...v1.11.1
[v1.11.0]: https://github.com/slackapi/bolt-python/compare/v1.10.0...v1.11.0
[v1.10.0]: https://github.com/slackapi/bolt-python/compare/v1.9.4...v1.10.0
[v1.9.4]: https://github.com/slackapi/bolt-python/compare/v1.9.3...v1.9.4
[v1.9.3]: https://github.com/slackapi/bolt-python/compare/v1.9.2...v1.9.3
[v1.9.2]: https://github.com/slackapi/bolt-python/compare/v1.9.1...v1.9.2
[v1.9.1]: https://github.com/slackapi/bolt-python/compare/v1.9.0...v1.9.1
[v1.9.0]: https://github.com/slackapi/bolt-python/compare/v1.8.1...v1.9.0
[v1.8.1]: https://github.com/slackapi/bolt-python/compare/v1.8.0...v1.8.1
[v1.8.0]: https://github.com/slackapi/bolt-python/compare/v1.8.0rc1...v1.8.0
[v1.8.0rc1]: https://github.com/slackapi/bolt-python/compare/v1.7.0...v1.8.0rc1
[v1.7.0]: https://github.com/slackapi/bolt-python/compare/v1.6.1...v1.7.0
[v1.6.1]: https://github.com/slackapi/bolt-python/compare/v1.6.0...v1.6.1
[v1.6.0]: https://github.com/slackapi/bolt-python/compare/v1.5.0...v1.6.0
[v1.5.0]: https://github.com/slackapi/bolt-python/compare/v1.4.4...v1.5.0
[v1.4.4]: https://github.com/slackapi/bolt-python/compare/v1.4.3...v1.4.4
[v1.4.3]: https://github.com/slackapi/bolt-python/compare/v1.4.2...v1.4.3
[v1.4.2]: https://github.com/slackapi/bolt-python/compare/v1.4.1...v1.4.2
[v1.4.1]: https://github.com/slackapi/bolt-python/compare/v1.4.0...v1.4.1
[v1.4.0]: https://github.com/slackapi/bolt-python/compare/v1.3.2...v1.4.0
[v1.3.2]: https://github.com/slackapi/bolt-python/compare/v1.3.1...v1.3.2
[v1.3.1]: https://github.com/slackapi/bolt-python/compare/v1.3.0...v1.3.1
[v1.3.0]: https://github.com/slackapi/bolt-python/compare/v1.2.3...v1.3.0
[v1.2.3]: https://github.com/slackapi/bolt-python/compare/v1.2.2...v1.2.3
[v1.2.2]: https://github.com/slackapi/bolt-python/compare/v1.2.1...v1.2.2
[v1.2.1]: https://github.com/slackapi/bolt-python/compare/v1.2.0...v1.2.1
[v1.2.0]: https://github.com/slackapi/bolt-python/compare/v1.1.5...v1.2.0
[v1.1.5]: https://github.com/slackapi/bolt-python/compare/v1.1.4...v1.1.5
[v1.1.4]: https://github.com/slackapi/bolt-python/compare/v1.1.3...v1.1.4
[v1.1.3]: https://github.com/slackapi/bolt-python/compare/v1.1.2...v1.1.3
[v1.1.2]: https://github.com/slackapi/bolt-python/compare/v1.1.1...v1.1.2
[v1.1.1]: https://github.com/slackapi/bolt-python/compare/v1.1.0...v1.1.1
[v1.1.0]: https://github.com/slackapi/bolt-python/compare/v1.1.0rc1...v1.1.0
[v1.1.0rc1]: https://github.com/slackapi/bolt-python/compare/v1.0.1...v1.1.0rc1
[v1.0.1]: https://github.com/slackapi/bolt-python/compare/v1.0.0...v1.0.1
[v1.0.0]: https://github.com/slackapi/bolt-python/compare/v1.0.0rc2...v1.0.0
[v1.0.0rc2]: https://github.com/slackapi/bolt-python/compare/v1.0.0rc1...v1.0.0rc2
[v1.0.0rc1]: https://github.com/slackapi/bolt-python/compare/v0.9.6b0...v1.0.0rc1
[v0.9.6b0]: https://github.com/slackapi/bolt-python/compare/v0.9.5b0...v0.9.6b0
[v0.9.5b0]: https://github.com/slackapi/bolt-python/compare/v0.9.4b0...v0.9.5b0
[v0.9.4b0]: https://github.com/slackapi/bolt-python/compare/v0.9.3b0...v0.9.4b0
[v0.9.3b0]: https://github.com/slackapi/bolt-python/compare/v0.9.2b0...v0.9.3b0
[v0.9.2b0]: https://github.com/slackapi/bolt-python/compare/v0.9.1b0...v0.9.2b0
[v0.9.1b0]: https://github.com/slackapi/bolt-python/compare/v0.9.0b0...v0.9.1b0
[v0.9.0b0]: https://github.com/slackapi/bolt-python/tree/v0.9.0b0

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.7.2 -->
