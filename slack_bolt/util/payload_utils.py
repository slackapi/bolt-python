from typing import Dict, Any, Optional


# ------------------------------------------
# Public Utilities
# ------------------------------------------

# -------------------
# Events API
# -------------------


def to_event(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload["event"] if is_event(payload) else None


def to_message(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if is_event(payload) and payload["event"]["type"] == "message":
        return to_event(payload)
    return None


def is_event(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "event_callback")
        and "event" in payload
        and "type" in payload["event"]
    )


# -------------------
# Slash Commands
# -------------------


def to_command(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload if is_slash_command(payload) else None


def is_slash_command(payload: Dict[str, Any]) -> bool:
    return payload is not None and "command" in payload


# -------------------
# Actions
# -------------------


def to_action(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if is_action(payload):
        if is_block_actions(payload):
            return payload["actions"][0]
        else:
            return payload
    return None


def is_action(payload: Dict[str, Any]) -> bool:
    return (
        is_attachment_action(payload)
        or is_block_actions(payload)
        or is_dialog_submission(payload)
        or is_dialog_cancellation(payload)
        or is_workflow_step_edit(payload)
    )


def is_attachment_action(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "interactive_message")
        and "callback_id" in payload
    )


def is_block_actions(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "block_actions")
        and "actions" in payload
    )


def is_dialog_submission(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "dialog_submission")
        and "callback_id" in payload
    )


def is_dialog_cancellation(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "dialog_cancellation")
        and "callback_id" in payload
    )


def is_workflow_step_edit(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "workflow_step_edit")
        and "callback_id" in payload
    )


# -------------------
# Options
# -------------------


def to_options(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if is_options(payload):
        return payload
    return None


def is_options(payload: Dict[str, Any]) -> bool:
    return is_block_suggestion(payload) or is_dialog_suggestion(payload)


def is_block_suggestion(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "block_suggestion")
        and "action_id" in payload
    )


def is_dialog_suggestion(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "dialog_suggestion")
        and "callback_id" in payload
    )


# -------------------
# Shortcut
# -------------------


def to_shortcut(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if is_shortcut(payload):
        return payload
    return None


def is_shortcut(payload: Dict[str, Any]) -> bool:
    return is_global_shortcut(payload) or is_message_shortcut(payload)


def is_global_shortcut(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "shortcut")
        and "callback_id" in payload
    )


def is_message_shortcut(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "message_action")
        and "callback_id" in payload
    )


# -------------------
# View
# -------------------


def to_view(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if is_view(payload):
        return payload["view"]
    return None


def is_view(payload: Dict[str, Any]) -> bool:
    return is_view_submission(payload) or is_view_closed(payload)


def is_view_submission(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "view_submission")
        and "view" in payload
        and "callback_id" in payload["view"]
    )


def is_view_closed(payload: Dict[str, Any]) -> bool:
    return (
        payload is not None
        and _is_expected_type(payload, "view_closed")
        and "view" in payload
        and "callback_id" in payload["view"]
    )


# ------------------------------------------
# Internal Utilities
# ------------------------------------------


def _is_expected_type(payload: dict, expected: str) -> bool:
    return payload is not None and "type" in payload and payload["type"] == expected
