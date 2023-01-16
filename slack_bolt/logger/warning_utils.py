def get_workflow_step_code_snippet(is_async: bool, callback_id: str) -> str:
    return f"""
from slack_bolt.workflows.step{'.async_step' if is_async else ''} import {'Async' if is_async else ''}WorkflowStep
ws = {'Async' if is_async else ''}WorkflowStep(
    callback_id="{callback_id}",
    edit=edit,
    save=save,
    execute=execute,
)
# Pass Step to set up listeners
app.step(ws)
"""


def get_action_code_snippet(is_async: bool, action_id_or_callback_id: str) -> str:
    return f"""
@app.action("{action_id_or_callback_id}")
{'async ' if is_async else ''}def handle_some_action(ack, body, logger):
    {'await ' if is_async else ''}ack()
    logger.info(body)
"""


def get_options_code_snippet(is_async: bool, constraints: str) -> str:
    return f"""
@app.options({constraints})
{'async ' if is_async else ''}def handle_some_options(ack):
    {'await ' if is_async else ''}ack(options=[ ... ])
"""


def get_shortcut_code_snippet(is_async: bool, id: str) -> str:
    return f"""
@app.shortcut("{id}")
{'async ' if is_async else ''}def handle_shortcuts(ack, body, logger):
    {'await ' if is_async else ''}ack()
    logger.info(body)
"""


def get_view_submission_code_snippet(is_async: bool, callback_id: str) -> str:
    return f"""
@app.view("{callback_id}")
{'async ' if is_async else ''}def handle_view_submission_events(ack, body, logger):
    {'await ' if is_async else ''}ack()
    logger.info(body)
"""


def get_view_closed_code_snippet(is_async: bool, callback_id: str) -> str:
    return f"""
@app.view_closed("{callback_id}")
{'async ' if is_async else ''}def handle_view_closed_events(ack, body, logger):
    {'await ' if is_async else ''}ack()
    logger.info(body)
"""


def get_function_code_snippet(is_async: bool, callback_id: str) -> str:
    return f"""
@app.function("{callback_id}")
{'async ' if is_async else ''}def handle_{callback_id}_function(body, complete_success, complete_error, logger):
    logger.info(body)
    complete_error("Function not implemented")
"""


def get_event_code_snippet(is_async: bool, event_type: str) -> str:
    return f"""
@app.event("{event_type}")
{'async ' if is_async else ''}def handle_{event_type}_events(body, logger):
    logger.info(body)
"""


def get_slash_command_code_snippet(is_async: bool, command: str) -> str:
    return f"""
@app.command("{command}")
{'async ' if is_async else ''}def handle_some_command(ack, body, logger):
    {'await ' if is_async else ''}ack()
    logger.info(body)
"""
