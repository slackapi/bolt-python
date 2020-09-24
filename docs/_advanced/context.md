---
title: Adding context
lang: en
slug: context
order: 7
---

<div class="section-content">
All listeners have access to a `context` dictionary, which can be used to enrich events with additional information. Bolt automatically attaches information if it’s included in the incoming event, like `user_id`, `team_id`, `channel_id`, and `enterprise_id`.

`context` is just a dictionary, so you can directly modify it.
</div>

```python
# Listener middleware to fetch tasks from external system using userId
def fetchTasks(context, event, next):
    user = event["user"]

    try:
        # Assume getTasks fetchs tasks from DB corresponding to user ID
        user_tasks = db.getTasks(user)
        tasks = user_tasks
    except Exception as e:
        # getTasks() raises exception because no tasks are found
        tasks = []
    finally:
        # Put user's tasks in context
        context["tasks"] = tasks
    next()

# Listener middleware to create a list of section blocks
def createSections(context, next)
    taskBlocks = []

    # Loops through tasks added to context in previous middleware
    for task in context["tasks"]:
        taskBlocks.append(
            {
              "type": "section",
              "text": {
                  "type": "mrkdwn",
                  "text": f"{task["title"]}\\n{task["body"]}"
              },
              "accessory": {
                  "type": "button",
                  "text": {
                    "type": "plain_text",
                    "text": "See task"
                  },
                  "url": task["url"],
                }
            }
        )

    # Put list of blocks in context
    context["blocks"] = taskBlocks

    next()

# Listen for user opening app home
# Include fetchTasks middleware
@app.event(
  "type"= "app_home_opened",
  "middleware"=[fetchTasks, createSections]
)
def showTasks(event, client, context):
    blocks=context.taskBlocks

    # Publish view to user's home tab
    client.views_publish(
        user=event["user"]
        view={
            "type": "home",
            "blocks": blocks
        }
    )
```