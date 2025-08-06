# Publishing views to App Home

[Home tabs](/surfaces/app-home) are customizable surfaces accessible via the sidebar and search that allow apps to display views on a per-user basis. After enabling App Home within your app configuration, home tabs can be published and updated by passing a `user_id` and [view payload](/reference/interaction-payloads/view-interactions-payload/#view_submission) to the [`views.publish`](/reference/methods/views.publish) method.

You can subscribe to the [`app_home_opened`](/reference/events/app_home_opened) event to listen for when users open your App Home.

Refer to [the module document](https://docs.slack.dev/tools/bolt-python/reference/kwargs_injection/args.html) to learn the available listener arguments.
```python
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # Call views.publish with the built-in client
        client.views_publish(
            # Use the user ID associated with the event
            user_id=event["user"],
            # Home tabs must be enabled in your app configuration
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome home, <@" + event["user"] + "> :house:*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                          "type": "mrkdwn",
                          "text": "Learn how home tabs can be more useful and interactive </surfaces/app-home|*in the documentation*>."
                        }
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
```